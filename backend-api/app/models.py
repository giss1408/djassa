from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func, Text, Boolean, Index
from sqlalchemy.orm import relationship
from .db import Base


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (
        Index("ix_payments_owner_created_at", "created_by", "created_at"),
        Index("ix_payments_external_status", "external_id", "status"),
    )
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric, nullable=False)
    currency = Column(String(8), nullable=False)
    recipient_id = Column(String(128), nullable=False)
    country_code = Column(String(2), nullable=False, default="CI")
    provider = Column(String(64), nullable=False, default="sandbox")
    external_id = Column(String(255), nullable=True, unique=True, index=True)
    checkout_url = Column(String(1024), nullable=True)
    idempotency_key = Column(String(128), nullable=True, unique=True, index=True)
    status = Column(String(32), nullable=False, default="created", index=True)
    provider_status = Column(String(32), nullable=True)
    error_code = Column(String(64), nullable=True)
    created_by = Column(String(128), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PaymentReconciliation(Base):
    __tablename__ = "payment_reconciliations"
    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=True, index=True)
    external_id = Column(String(255), nullable=False, index=True)
    provider = Column(String(64), nullable=False)
    provider_status = Column(String(32), nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(String(8), nullable=False)
    raw_reference = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PaymentRefund(Base):
    __tablename__ = "payment_refunds"
    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False, index=True)
    amount = Column(Numeric, nullable=False)
    idempotency_key = Column(String(128), nullable=False, unique=True)
    external_id = Column(String(255), nullable=True, unique=True)
    status = Column(String(32), nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PaymentDispute(Base):
    __tablename__ = "payment_disputes"
    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False, index=True)
    reason = Column(String(255), nullable=False)
    status = Column(String(32), nullable=False, default="open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Merchant(Base):
    __tablename__ = "merchants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    external_id = Column(String(255), nullable=True, unique=True)
    description = Column(Text, nullable=True)
    # relationships
    transactions = relationship("Transaction", back_populates="merchant")


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        Index("ix_transactions_merchant_timestamp", "merchant_id", "timestamp"),
        Index("ix_transactions_merchant_user_timestamp", "merchant_id", "user_id", "timestamp"),
    )
    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=False, index=True)
    user_id = Column(String(128), nullable=True, index=True)
    amount = Column(Numeric, nullable=False)
    currency = Column(String(8), nullable=False)
    type = Column(String(32), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    idempotency_key = Column(String(128), nullable=True, unique=True, index=True)
    idempotency_hash = Column(String(64), nullable=True)

    merchant = relationship("Merchant", back_populates="transactions")


class Consent(Base):
    __tablename__ = "consents"
    __table_args__ = (Index("ix_consents_user_merchant_scope", "user_id", "merchant_id", "scope"),)
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(128), nullable=False, index=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=False)
    scope = Column(String(255), nullable=False)
    granted_at = Column(DateTime(timezone=True), server_default=func.now())

    merchant = relationship("Merchant")


class TontineGroup(Base):
    __tablename__ = "tontine_groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    organizer_id = Column(String(128), nullable=False, index=True)
    contribution_amount = Column(Numeric, nullable=False)
    currency = Column(String(8), nullable=False, default="XOF")
    frequency = Column(String(32), nullable=False, default="monthly")
    max_members = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    members = relationship("TontineMember", back_populates="group")
    cycles = relationship("TontineCycle", back_populates="group")


class TontineMember(Base):
    __tablename__ = "tontine_members"
    __table_args__ = (Index("ix_tontine_members_group_user_active", "group_id", "user_id", "active"),)
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("tontine_groups.id"), nullable=False, index=True)
    user_id = Column(String(128), nullable=False, index=True)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    is_admin = Column(Boolean, default=False)
    active = Column(Boolean, default=True)

    group = relationship("TontineGroup", back_populates="members")
    contributions = relationship("Contribution", back_populates="member")


class TontineCycle(Base):
    __tablename__ = "tontine_cycles"
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("tontine_groups.id"), nullable=False, index=True)
    cycle_number = Column(Integer, nullable=False, default=1)
    start_at = Column(DateTime(timezone=True), nullable=True)
    end_at = Column(DateTime(timezone=True), nullable=True)
    payout_member_id = Column(Integer, ForeignKey("tontine_members.id"), nullable=True)
    status = Column(String(32), nullable=False, default="open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    group = relationship("TontineGroup", back_populates="cycles")
    contributions = relationship("Contribution", back_populates="cycle")


class Contribution(Base):
    __tablename__ = "tontine_contributions"
    __table_args__ = (Index("ix_contributions_group_member_paid_at", "group_id", "member_id", "paid_at"),)
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("tontine_groups.id"), nullable=False, index=True)
    cycle_id = Column(Integer, ForeignKey("tontine_cycles.id"), nullable=True, index=True)
    member_id = Column(Integer, ForeignKey("tontine_members.id"), nullable=False, index=True)
    amount = Column(Numeric, nullable=False)
    currency = Column(String(8), nullable=False)
    paid_at = Column(DateTime(timezone=True), server_default=func.now())
    payment_reference = Column(String(255), nullable=True)
    status = Column(String(32), nullable=False, default="received")

    member = relationship("TontineMember", back_populates="contributions")
    cycle = relationship("TontineCycle", back_populates="contributions")


class WebhookEvent(Base):
    __tablename__ = "webhook_events"
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(255), nullable=False, unique=False, index=True)
    payload = Column(Text, nullable=False)
    received_at = Column(DateTime(timezone=True), server_default=func.now())


class WebhookProcessingLog(Base):
    __tablename__ = "webhook_processing_log"
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(255), nullable=False, index=True)
    status = Column(String(50), nullable=False)
    processed_at = Column(DateTime(timezone=True), server_default=func.now())


class WebhookIdempotency(Base):
    __tablename__ = "webhook_idempotency"
    external_id = Column(String(255), primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    expires_at = Column(DateTime(timezone=True), nullable=True, index=True)


class SupportRequest(Base):
    __tablename__ = "support_requests"
    __table_args__ = (
        Index("ix_support_requests_user_created_at", "user_id", "created_at"),
        Index("ix_support_requests_country_status", "country_code", "status"),
    )
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(128), nullable=False, index=True)
    country_code = Column(String(2), nullable=False)
    language = Column(String(16), nullable=False)
    channel = Column(String(32), nullable=False)
    category = Column(String(64), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(32), nullable=False, default="open", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

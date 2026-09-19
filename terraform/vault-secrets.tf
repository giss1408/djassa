provider "vault" {
  address = var.vault_addr
  token   = var.vault_token
}

resource "vault_policy" "djassa_read" {
  name   = "djassa-read"
  policy = file("../vault/demo-policy.hcl")
}

resource "vault_generic_secret" "djassa_database" {
  path = "secret/data/djassa/database"
  data_json = jsonencode({
    url = var.database_url
  })
}

resource "vault_generic_secret" "djassa_mobile_money" {
  path = "secret/data/djassa/mobile_money"
  data_json = jsonencode({
    secret = var.mobile_money_secret
  })
}

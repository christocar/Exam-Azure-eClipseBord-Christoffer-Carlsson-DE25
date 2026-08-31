variable "project_name" {
  type    = string
  default = "eclipsebord"
}

variable "location" {
  type    = string
  default = "norwayeast"
}

# ACR names are globally unique across all of Azure, so this needs to be yours
variable "unique_suffix" {
  type    = string
  default = "chr01"
}
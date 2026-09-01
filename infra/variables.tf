# used as a prefix for every resource name, so they're easy to spot in the portal
variable "project_name" {
  type    = string
  default = "eclipsebord"
}

# denmarkeast because the student subscription had no B1 quota in norwayeast
# quotas are per region, so this is the one setting to change if a deploy fails
variable "location" {
  type    = string
  default = "denmarkeast"
}

# ACR names are globally unique across all of Azure, so this needs to be yours
# lowercase letters and digits only, no dashes
variable "unique_suffix" {
  type    = string
  default = "chr01"
}
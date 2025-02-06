ipmi = {
    "username": "string",
    "auth_password": "string"
}

snmpv3 = {
    "community": "string"
}

snmpv3_noauth = {
    "username":"string",
    "security_level":"noauth"    
}


snmpv3_noprv = {
    "username":"string",
    "security_level":"noprv",    
    "auth_encryption":"5 вариантов",    
    "auth_password":"string"
    "contextname": "optional"
}


snmpv3_prv = {
    "username":"string",
    "security_level":"prv",    
    "auth_encryption":"5 вариантов",    
    "auth_password":"string",
    "privacy_encryption":"4 варианта",
    "privacy_password":"string"
    "contextname": "optional"
}

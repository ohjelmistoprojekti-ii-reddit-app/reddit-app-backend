user_schema = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/product.schema.json",
  "title": "NewUser",
  "type": "object",
  "properties": {
    "username": {
      "type": "string",
      "minLength": 3,
      "maxLength": 20,
      "validationMessage": "Username must be from 3 to 20 characters"
    },
    "email": {
      "type": "string",
      "pattern": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$",
      "validationMessage": "Invalid email format"
    },
    "password": {
      "type": "string",
      "minLength": 8,
      "validationMessage": "Password must be at least 8 characters"
    },
    "last_login": {
      "type": ["string", "null"],
      "format": "date-time"
    },
    "revoked_access_tokens": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "refresh_revoked": {
      "type": "boolean"
    }
  },
  "required": [
    "username",
    "email",
    "password",
    "last_login",
    "revoked_access_tokens",
    "refresh_revoked"
  ]
}
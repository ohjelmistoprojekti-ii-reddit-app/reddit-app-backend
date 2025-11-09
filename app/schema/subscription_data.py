{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/product.schema.json",
  "title": "subscription_data",
  "type": "object",
  "properties": {
    "_id": {
      "type": "string",
      "pattern": "^[a-f0-9]{24}$"
    },
    "posts": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "comments": {
            "type": "array",
            "items": { "type": "string" }
          },
          "content": {
            "type": "string"
          },
          "content_link": {
            "type": "string",
            "format": "uri"
          },
          "link": {
            "type": "string",
            "format": "uri"
          },
          "num_comments": {
            "type": "integer",
            "minimum": 0
          },
          "score": {
            "type": "integer"
          },
          "sentiment_values": {
            "type": "object",
            "properties": {
              "average_compound": { "type": "number" },
              "average_neg": { "type": "number" },
              "average_neu": { "type": "number" },
              "average_pos": { "type": "number" }
            },
            "required": [
              "average_compound",
              "average_neg",
              "average_neu",
              "average_pos"
            ]
          },
          "title": {
            "type": "string"
          }
        },
        "required": [
          "comments",
          "content_link",
          "link",
          "num_comments",
          "score",
          "sentiment_values",
          "title"
        ]
      }
    },
    "subreddit": {
      "type": "string"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "type": {
      "type": "string",
      "enum": ["posts"]
    }
  },
  "required": [
    "_id",
    "posts",
    "subreddit",
    "timestamp",
    "type"
  ]
}
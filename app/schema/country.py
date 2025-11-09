{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/product.schema.json",
  "title": "Country",
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "_id": {
        "type": "string",
        "pattern": "^[a-f0-9]{24}$"
      },
      "country_id": {
        "type": "string",
        "minLength": 2,
        "maxLength": 3
      },
      "country_name": {
        "type": "string"
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
            "comments_eng": {
              "type": "array",
              "items": { "type": "string" }
            },
            "content": {
              "type": "string"
            },
            "content_eng": {
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
            },
            "title_eng": {
              "type": "string"
            }
          },
          "required": [
            "comments",
            "comments_eng",
            "content_link",
            "link",
            "num_comments",
            "score",
            "sentiment_values",
            "title",
            "title_eng"
          ]
        }
      },
      "subreddit": {
        "type": "string"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time"
      }
    },
    "required": [
      "_id",
      "country_id",
      "country_name",
      "posts",
      "subreddit",
      "timestamp"
    ]
  }
}
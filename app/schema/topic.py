{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/product.schema.json",
  "title": "Topic",
  "type": "object",
  "properties": {
    "_id": {
      "type": "string",
      "pattern": "^[a-f0-9]{24}$"
    },
    "id": {
      "type": "integer"
    },
    "num_posts": {
      "type": "integer",
      "minimum": 0
    },
    "posts": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "comments": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "content": {
            "type": "string"
          },
          "created_at": {
            "type": "string",
            "format": "date-time"
          },
          "id": {
            "type": "string"
          },
          "num_comments": {
            "type": "integer",
            "minimum": 0
          },
          "score": {
            "type": "integer"
          },
          "subreddit": {
            "type": "string"
          },
          "title": {
            "type": "string"
          },
          "upvote_ratio": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        },
        "required": [
          "comments",
          "created_at",
          "id",
          "num_comments",
          "score",
          "subreddit",
          "title",
          "upvote_ratio"
        ]
      }
    },
    "sentiment_values": {
      "type": "object",
      "properties": {
        "average_compound": { "type": "number" },
        "average_neg": { "type": "number" },
        "average_neu": { "type": "number" },
        "average_pos": { "type": "number" },
        "comment_count": { "type": "integer", "minimum": 0 }
      },
      "required": [
        "average_compound",
        "average_neg",
        "average_neu",
        "average_pos",
        "comment_count"
      ]
    },
    "subreddit": {
      "type": "string"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "topic": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  },
  "required": [
    "_id",
    "id",
    "num_posts",
    "posts",
    "sentiment_values",
    "subreddit",
    "timestamp",
    "topic"
  ]
}
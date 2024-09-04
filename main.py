{
  "version": "1.0.0",
  "name": "AI Scaffolding Strategist API",
  "description": "This API allows users to interact with the AI Scaffolding Strategist, guiding non-programmers step-by-step through the process of building automated systems.",
  "servers": [
    {
      "url": "https://api.yourdomain.com",
      "description": "Production server"
    },
    {
      "url": "https://staging.api.yourdomain.com",
      "description": "Staging server"
    }
  ],
  "endpoints": [
    {
      "name": "Start Session",
      "description": "Initiates a new session and returns a session ID.",
      "url": "/api/startSession",
      "method": "POST",
      "parameters": [],
      "response": {
        "session_id": "string",
        "status": "string",
        "started_at": "string"
      }
    },
    {
      "name": "Get Next Question",
      "description": "Fetches the next question in the sequence for the user based on their current session progress.",
      "url": "/api/questions",
      "method": "GET",
      "parameters": [
        {
          "name": "session_id",
          "type": "string",
          "description": "The ID of the session to fetch the next question for."
        }
      ],
      "response": {
        "question": "string",
        "options": ["string"]
      }
    },
    {
      "name": "Submit Answer",
      "description": "Submits an answer to the current question and moves the user to the next step.",
      "url": "/api/answers",
      "method": "POST",
      "parameters": [
        {
          "name": "session_id",
          "type": "string",
          "description": "The ID of the session associated with this answer."
        },
        {
          "name": "answer",
          "type": "string",
          "description": "The user's answer to the current question."
        }
      ],
      "response": {
        "status": "string"
      }
    },
    {
      "name": "Get Progress",
      "description": "Retrieves the current progress, listing completed and pending questions.",
      "url": "/api/progress",
      "method": "GET",
      "parameters": [
        {
          "name": "session_id",
          "type": "string",
          "description": "The ID of the session to fetch progress for."
        }
      ],
      "response": {
        "completedSteps": ["string"],
        "pendingSteps": ["string"]
      }
    },
    {
      "name": "Get Review",
      "description": "Provides a summary of all the answers submitted so far.",
      "url": "/api/review",
      "method": "GET",
      "parameters": [
        {
          "name": "session_id",
          "type": "string",
          "description": "The ID of the session to review."
        }
      ],
      "response": {
        "question": "string",
        "options": []
      }
    },
    {
      "name": "Suggest Action",
      "description": "Suggests the next best action based on the user's session data.",
      "url": "/api/suggestAction",
      "method": "POST",
      "parameters": [
        {
          "name": "session_id",
          "type": "string",
          "description": "The ID of the session to suggest an action for."
        }
      ],
      "response": {
        "suggested_action": "string",
        "status": "string",
        "reason": "string"
      }
    }
  ]
}

# Advanced Features Guide

The Mem0 MCP Server includes several advanced features that enhance the basic memory operations. This guide explains these features and provides examples of how to use them effectively.

## Custom Categories

Custom categories allow you to organize semantic memories in a way that makes sense for your specific use case.

### Setting Custom Categories

```python
# Define custom categories
custom_categories = [
    {"project_knowledge": "Information specific to project structure and architecture"},
    {"coding_standards": "Preferred coding practices and standards"},
    {"ui_preferences": "User interface design preferences"},
    {"scheduling": "Time and scheduling preferences"}
]

# Update the categories
result = await mem0_update_categories(custom_categories)
```

### Retrieving Current Categories

```python
# Get the current categories
categories = await mem0_get_categories()
```

### Using Categories with Semantic Memory

```python
# Add a semantic memory with a custom category
result = await mem0_add_semantic_memory(
    text="The project follows a microservices architecture with separate services for auth, content, and analytics.",
    user_id="richard_yaker",
    category="project_knowledge"
)
```

### Best Practices

- Limit the number of categories to maintain clarity
- Provide clear descriptions for each category
- Use consistent naming conventions
- Review and update categories as your project evolves

## Selective Memory with Includes/Excludes

Selective memory allows you to control what parts of a text are processed and stored, using pattern matching.

### Using Includes Pattern

```python
# Store only code blocks from technical documentation
result = await mem0_add_memory_selective(
    text="# Setting Up the Project\n\nFollow these steps:\n\n```python\nimport os\nos.environ['DEBUG'] = 'True'\n```\n\nThis will enable debug mode.",
    user_id="richard_yaker",
    includes="```python.*?```",  # Only store Python code blocks
    metadata={"topic": "setup_instructions"}
)
```

### Using Excludes Pattern

```python
# Store everything except personal information
result = await mem0_add_memory_selective(
    text="My API key is ABC123XYZ. The application should be configured to use the production database.",
    user_id="richard_yaker",
    excludes="API key is .*?\\.",  # Exclude the API key
    metadata={"topic": "configuration"}
)
```

### Combining Includes and Excludes

```python
# Complex filtering example
result = await mem0_add_memory_selective(
    text="User: John (john@example.com)\nPreferences: Dark mode, auto-save every 5 min\nSettings: API endpoint is https://api.example.com",
    user_id="richard_yaker",
    includes="Preferences:.*?\\n|Settings:.*?\\n",  # Only include preferences and settings
    excludes="john@example\\.com",  # Exclude email
    metadata={"topic": "user_configuration"}
)
```

### Best Practices

- Test your regex patterns before using them in production
- Use includes for extracting specific content types
- Use excludes for filtering out sensitive information
- Remember that includes takes precedence over excludes

## Custom Instructions

Custom instructions provide guidelines for memory processing and extraction.

### Setting Instructions

```python
# Set custom instructions
instructions = """
When processing memories:
1. Extract technical terms and tag them with [TECH]
2. Format code blocks with language identifier
3. Separate factual information from opinions
4. Extract action items and tag them with [ACTION]
5. Identify questions and tag them with [QUESTION]
"""

result = await mem0_set_instructions(instructions)
```

### Retrieving Instructions

```python
# Get the current instructions
current_instructions = await mem0_get_instructions()
```

### Best Practices

- Keep instructions clear and specific
- Update instructions as your memory usage evolves
- Share instructions with team members for consistency
- Review the effect of instructions periodically

## Graph Memory Relations

The graph memory feature allows you to establish and explore relationships between different memories and entities.

### Enabling Graph Processing

```python
# Enable graph processing when adding a memory
result = await mem0_add_memory(
    text="React was created by Facebook and is maintained by Meta.",
    user_id="richard_yaker",
    enable_graph=True,
    metadata={"topic": "technology"}
)
```

### Querying Graph Relationships

```python
# Query all relationships for an entity
relations = await mem0_get_graph_relations(
    user_id="richard_yaker",
    entity="React"
)

# Query specific relationship types
created_by_relations = await mem0_get_graph_relations(
    user_id="richard_yaker",
    entity="React",
    relation_type="created_by"
)
```

### Visualizing the Knowledge Graph

While the MCP server doesn't provide direct visualization, the returned graph data can be used with visualization libraries or tools.

Example returned format:
```json
{
  "nodes": [
    {"id": "React", "type": "Technology"},
    {"id": "Facebook", "type": "Organization"},
    {"id": "Meta", "type": "Organization"}
  ],
  "edges": [
    {"source": "React", "target": "Facebook", "relation": "created_by"},
    {"source": "React", "target": "Meta", "relation": "maintained_by"}
  ]
}
```

### Best Practices

- Enable graph processing for factual, relationship-rich content
- Use semantic memories for optimal graph extraction
- Query specific relationship types to avoid overwhelming results
- Use consistent entity naming for better detection

## Memory Feedback Mechanism

The feedback mechanism allows you to provide feedback on memory quality, helping to improve memory processing and retrieval.

### Providing Feedback

```python
# Find a memory to provide feedback on
search_result = await mem0_search_memory(
    query="project architecture",
    user_id="richard_yaker"
)

# Get the memory ID from the search results
memory_id = search_result["results"][0]["id"]

# Provide positive feedback
result = await mem0_send_feedback(
    memory_id=memory_id,
    feedback_type="helpful",
    comments="This memory provided exactly the information I needed about our architecture"
)
```

### Feedback Types

- `helpful`: The memory was useful and accurate
- `not_helpful`: The memory was not useful or contains errors
- `irrelevant`: The memory was not relevant to the context
- `outdated`: The memory contains outdated information
- `incomplete`: The memory is missing important details

### Using Feedback for Improvement

Feedback can help you:
1. Identify which memories are most valuable
2. Highlight memories that need updating
3. Improve the quality of your memory corpus over time
4. Train better retrieval models based on user preferences

### Best Practices

- Provide specific comments with your feedback
- Follow up negative feedback with updated memories
- Use feedback consistently as part of your workflow
- Review feedback trends to improve memory creation

## Combining Advanced Features

These advanced features can be combined for powerful memory management:

### Example: Comprehensive Knowledge Base

```python
# 1. Set up custom categories
await mem0_update_categories([
    {"code_patterns": "Coding patterns and practices"},
    {"architecture": "System architecture information"},
    {"api_usage": "API usage examples and notes"}
])

# 2. Set up custom instructions
await mem0_set_instructions("""
Extract code examples, API endpoints, and architecture decisions.
Format code with language tags and indent properly.
""")

# 3. Add selective memory with graph processing
await mem0_add_memory_selective(
    text="Our system uses a REST API at https://api.example.com/v2/. Authentication uses Bearer tokens. Example:\n```javascript\nfetch('https://api.example.com/v2/users', {\n  headers: { Authorization: 'Bearer TOKEN' }\n})```",
    user_id="richard_yaker",
    includes="(https://.*?/)|```javascript.*?```",
    enable_graph=True,
    metadata={"topic": "api_documentation"}
)

# 4. Provide feedback on quality
await mem0_send_feedback(
    memory_id="some_memory_id",
    feedback_type="helpful",
    comments="Great API documentation example"
)
```

## Performance Considerations

When using advanced features, be aware of these performance implications:

- Graph processing adds processing time but enhances relationship discovery
- Complex regex patterns in selective memory may increase processing time
- Extensive custom instructions may slow down memory processing
- Using multiple advanced features together might impact performance

For optimal performance, monitor memory operations and adjust feature usage accordingly. 
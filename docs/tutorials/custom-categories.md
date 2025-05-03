# Tutorial: Setting Up Custom Memory Categories

This tutorial guides you through the process of creating, updating, and using custom memory categories in the Mem0 MCP Server.

## What Are Custom Categories?

Custom categories allow you to organize your semantic memories in a way that makes sense for your specific use case. Instead of using default categories, you can define your own categories that reflect your project's needs, preferences, or knowledge domains.

## Benefits of Custom Categories

- **Better Organization**: Group memories in a way that makes sense for your specific needs
- **Improved Retrieval**: Find relevant memories more easily with appropriate categorization
- **Domain-Specific Knowledge**: Create categories that match your field or project
- **Consistent Structure**: Maintain a coherent organization system for your memories

## Step 1: Define Your Categories

First, think about what categories would be most useful for your project. Categories should:

- Be descriptive but concise
- Cover distinct areas without too much overlap
- Be limited to a manageable number (5-10 is often ideal)
- Include clear descriptions

Example categories for a software development project:

```python
custom_categories = [
    {"architecture": "System architecture and design patterns"},
    {"coding_standards": "Code style and programming best practices"},
    {"project_setup": "Environment configuration and project initialization"},
    {"deployment": "Deployment processes and infrastructure details"},
    {"user_experience": "UI/UX guidelines and principles"}
]
```

Example categories for a research project:

```python
custom_categories = [
    {"methodology": "Research methods and experimental design"},
    {"literature": "Key papers and literature review notes"},
    {"findings": "Research results and data insights"},
    {"theories": "Theoretical frameworks and concepts"},
    {"future_work": "Ideas for follow-up research"}
]
```

## Step 2: Update Your Categories

Once you've defined your categories, use the `mem0_update_categories` tool to update them in the Mem0 system:

```
Update my memory categories using mem0_update_categories with the following categories:
[
    {"architecture": "System architecture and design patterns"},
    {"coding_standards": "Code style and programming best practices"},
    {"project_setup": "Environment configuration and project initialization"},
    {"deployment": "Deployment processes and infrastructure details"},
    {"user_experience": "UI/UX guidelines and principles"}
]
```

The system will confirm when your categories have been updated.

## Step 3: Verify Your Categories

You can check your current categories at any time using the `mem0_get_categories` tool:

```
Show me my current memory categories using mem0_get_categories.
```

The response will show all your current categories with their descriptions.

## Step 4: Use Categories with Semantic Memories

Now you can use your custom categories when adding semantic memories:

```
Add to my semantic memory using mem0_add_semantic_memory: 
"The project uses a microservices architecture with separate services for user management, content delivery, and analytics."
with user_id "your-user-id", category "architecture".
```

The memory will be stored with the specified category, making it easier to organize and retrieve related information later.

## Step 5: Search Within Categories

When searching for memories, you can filter by category using the `filters` parameter:

```
Search my memories for "microservices" using mem0_search_memory with 
user_id "your-user-id" and filters '{"metadata.category": "architecture"}'.
```

This will return only memories in the "architecture" category that match your search query.

## Step 6: Update Categories as Needed

As your project evolves, you may need to update your categories. You can add, modify, or remove categories at any time using the `mem0_update_categories` tool. Just be aware that this will replace your entire category set.

To modify a single category while keeping others:
1. Get your current categories with `mem0_get_categories`
2. Make the necessary changes to the retrieved list
3. Update all categories with your modified list using `mem0_update_categories`

## Best Practices

1. **Be Consistent**: Use categories consistently for all relevant memories
2. **Review Periodically**: Revisit your categories periodically to ensure they remain relevant
3. **Don't Overdo It**: Keep the number of categories manageable
4. **Use Clear Descriptions**: Write clear descriptions to help differentiate similar categories
5. **Consider User Needs**: Design categories around how users will want to find information

## Example Workflow

Here's a complete example of working with custom categories:

```
# 1. Set up custom categories
Update my memory categories using mem0_update_categories with the following categories:
[
    {"tech_stack": "Technologies, frameworks, and libraries used in the project"},
    {"api_design": "API endpoints, parameters, and response structures"},
    {"dev_environment": "Development environment setup and configuration"},
    {"troubleshooting": "Common issues and their resolutions"},
    {"performance": "Performance optimization techniques and benchmarks"}
]

# 2. Verify the categories
Show me my current memory categories using mem0_get_categories.

# 3. Add memories with categories
Add to my semantic memory using mem0_add_semantic_memory: 
"The project uses React for the frontend and Django for the backend API."
with user_id "your-user-id", category "tech_stack".

Add to my semantic memory using mem0_add_semantic_memory:
"API rate limiting is set to 100 requests per minute per user."
with user_id "your-user-id", category "api_design".

Add to my semantic memory using mem0_add_semantic_memory:
"Run npm run dev to start the development server with hot reloading."
with user_id "your-user-id", category "dev_environment".

# 4. Search within a category
Search my memories for "API" using mem0_search_memory with 
user_id "your-user-id" and filters '{"metadata.category": "api_design"}'.
```

This workflow establishes a set of categories relevant to a software project, verifies they are set correctly, adds memories with appropriate categorization, and demonstrates how to search within a specific category.

## Conclusion

Custom categories are a powerful way to organize your semantic memories according to your specific needs. By taking the time to design an appropriate category system and using it consistently, you can significantly improve how you store and retrieve knowledge in your Mem0 MCP Server. 
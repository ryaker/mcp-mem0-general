# MCP Mem0 General Server - Usage Guide

This guide details the tools provided by the MCP Mem0 General Server and provides example prompts for using them with Claude Desktop.

**Important:**

*   Replace `"your_user_id"` in the examples with a unique identifier for yourself (e.g., `"default_user"`). Consistency is key for Mem0 to associate memories correctly.
*   For features like Graph Memory, ensure your Mem0 plan supports it.
*   Refer to the [Mem0 Documentation](https://docs.mem0.ai/) for more in-depth details on concepts like filters, metadata structure, etc.

## Tools

### 1. `mem0_add_memory`

Adds a new memory or updates existing memories based on the provided text and context.

**Parameters:**

*   `text` (str): The text containing the information to be stored.
*   `user_id` (str | None): **Required.** A unique identifier for the user.
*   `agent_id` (str | None): Optional identifier for the AI agent.
*   `run_id` (str | None): Optional identifier for the current conversation session.
*   `metadata` (dict | None): Optional dictionary of key-value pairs to store alongside the memory.
*   `enable_graph` (bool): Optional (Default: `False`). Set to `True` to enable graph memory processing (requires Pro plan).
*   `includes` (str | None): Optional. Comma-separated keywords. Only sentences containing these keywords will be considered for memory.
*   `excludes` (str | None): Optional. Comma-separated keywords. Sentences containing these keywords will be excluded from memory consideration.
*   `timestamp` (int | None): Optional. Unix timestamp (integer) to set a custom creation time for the memory.
*   `expiration_date` (str | None): Optional. ISO 8601 formatted string (e.g., `"2025-12-31T23:59:59Z"`) to set an expiration time.

**Example Prompts (Claude Desktop):**

*   **Simple Add:**
    ```
    Please remember that my favorite color is blue.
    (Claude calls mem0_add_memory with text="My favorite color is blue", user_id="default_user")
    ```

*   **Add with Metadata:**
    ```
    Remember this project detail: The deadline for project 'Alpha' is next Friday. Associate this with category 'work' and priority 'high'.
    (Claude calls mem0_add_memory with text="The deadline for project 'Alpha' is next Friday.", user_id="default_user", metadata={"category": "work", "priority": "high"})
    ```

*   **Add with Graph Enabled:**
    ```
    Please remember this relationship using graph features: Alice reports to Bob.
    (Claude calls mem0_add_memory with text="Alice reports to Bob.", user_id="default_user", enable_graph=True)
    ```

*   **Add with Timestamp:**
    ```
    Log this event as occurring on January 1st, 2024: We signed the contract.
    (Claude calculates timestamp for Jan 1, 2024, e.g., 1704067200, then calls mem0_add_memory with text="We signed the contract.", user_id="default_user", timestamp=1704067200)
    ```

*   **Add with Expiration:**
    ```
    Remember that the promo code 'SAVE10' is valid until the end of this month. Set it to expire automatically.
    (Claude calculates the expiration date string for end-of-month, e.g., "2025-05-31T23:59:59Z", then calls mem0_add_memory with text="Promo code 'SAVE10' is valid until end of month.", user_id="default_user", expiration_date="2025-05-31T23:59:59Z")
    ```

*   **Add with Selective Memory (Includes):**
    ```
    Store this conversation summary, but only focus on the parts mentioning 'budget' and 'timeline': [conversation text here...]
    (Claude calls mem0_add_memory with text="[conversation text here...]", user_id="default_user", includes="budget,timeline")
    ```

### 2. `mem0_search_memory`

Searches for memories relevant to a query, optionally applying filters and graph retrieval.

**Parameters:**

*   `query` (str): The search query.
*   `user_id` (str | None): **Required.** The user identifier to scope the search.
*   `agent_id` (str | None): Optional agent identifier to filter search.
*   `run_id` (str | None): Optional run identifier to filter search.
*   `filters` (str | None): Optional JSON string representing a filter dictionary (see [Mem0 Search Filters](https://docs.mem0.ai/platform/quickstart#search-using-custom-filters) for structure).
*   `threshold` (float | None): Optional. Minimum similarity score (0.0 to 1.0) for results.
*   `enable_graph` (bool): Optional (Default: `False`). Set to `True` to use graph retrieval.

**Example Prompts (Claude Desktop):**

*   **Simple Search:**
    ```
    What do you remember about my favorite color?
    (Claude calls mem0_search_memory with query="my favorite color", user_id="default_user")
    ```

*   **Search with Graph:**
    ```
    Tell me about the relationships you know regarding Alice (use graph search).
    (Claude calls mem0_search_memory with query="relationships regarding Alice", user_id="default_user", enable_graph=True)
    ```

*   **Search with Filters (Metadata):**
    ```
    Find memories related to 'project deadlines' in the 'work' category.
    (Claude constructs filter JSON string: '{"metadata": {"category": "work"}}' then calls mem0_search_memory with query="project deadlines", user_id="default_user", filters='{"metadata": {"category": "work"}}')
    ```
    *Note: Claude needs to correctly format the dictionary into a JSON string for the `filters` parameter.* 

*   **Search with Threshold:**
    ```
    Search for memories about 'vacation plans', but only show highly relevant results.
    (Claude calls mem0_search_memory with query="vacation plans", user_id="default_user", threshold=0.8)
    ```

### 3. `mem0_get_all_memories`

Retrieves all memories, optionally filtered by ID and paginated.

**Parameters:**

*   `user_id` (str | None): Optional. Filter by user ID.
*   `agent_id` (str | None): Optional. Filter by agent ID.
*   `run_id` (str | None): Optional. Filter by run ID.
*   `limit` (int | None): Optional. Maximum number of memories (potentially conflicts with pagination).
*   `page` (int | None): Optional. Page number for pagination (starts at 1).
*   `page_size` (int | None): Optional. Number of memories per page.
*   `enable_graph` (bool): Optional (Default: `False`). Include graph context in results.

**Example Prompts (Claude Desktop):**

*   **Get All for User:**
    ```
    List all memories you have stored for me.
    (Claude calls mem0_get_all_memories with user_id="default_user")
    ```

*   **Get All with Pagination:**
    ```
    Show me the first 10 memories you have for me.
    (Claude calls mem0_get_all_memories with user_id="default_user", page=1, page_size=10)
    ```

*   **Get All for Session:**
    ```
    List the memories created during this specific session run.
    (Claude needs the current run_id, e.g., "run123", then calls mem0_get_all_memories with user_id="default_user", run_id="run123")
    ```

### 4. `mem0_get_memory_by_id`

Retrieves a single, specific memory using its unique ID.

**Parameters:**

*   `memory_id` (str): **Required.** The unique ID of the memory to retrieve.

**Example Prompts (Claude Desktop):**

*   **Get Specific Memory:**
    ```
    Show me the details of memory with ID 'abc-123-def-456'.
    (Claude calls mem0_get_memory_by_id with memory_id="abc-123-def-456")
    ```
    *(Claude would typically get this ID from a previous search or listing result).* 

### 5. `mem0_update_memory`

Updates the text content of an existing memory.

**Parameters:**

*   `memory_id` (str): **Required.** The ID of the memory to update.
*   `text` (str): **Required.** The new text content for the memory.

**Example Prompts (Claude Desktop):**

*   **Update Memory:**
    ```
    Update memory 'xyz-789': Change the deadline for project 'Alpha' to *two* Fridays from now.
    (Claude calls mem0_update_memory with memory_id="xyz-789", text="The deadline for project 'Alpha' is two Fridays from now.")
    ```
    *(Claude would typically get the memory_id from a prior search/get).* 

### 6. `mem0_delete_memory`

Deletes a specific memory by its ID.

**Parameters:**

*   `memory_id` (str): **Required.** The ID of the memory to delete.

**Example Prompts (Claude Desktop):**

*   **Delete Memory:**
    ```
    Please delete memory 'def-456'.
    (Claude calls mem0_delete_memory with memory_id="def-456")
    ```
    *(Claude would typically get the memory_id from a prior search/get).* 

### 7. `mem0_count_memories`

Counts the number of memories, optionally applying filters.

**Parameters:**

*   `user_id` (str | None): **Required.** The user identifier to scope the count.
*   `agent_id` (str | None): Optional agent identifier to filter count.
*   `run_id` (str | None): Optional run identifier to filter count.
*   `filters` (dict | None): Optional dictionary of filters (similar structure to search filters, but passed as a dict).

**Example Prompts (Claude Desktop):**

*   **Count All for User:**
    ```
    How many memories do you have stored for me in total?
    (Claude calls mem0_count_memories with user_id="default_user")
    ```

*   **Count with Filters:**
    ```
    Count how many memories I have in the 'work' category.
    (Claude calls mem0_count_memories with user_id="default_user", filters={"metadata": {"category": "work"}})
    ``` 
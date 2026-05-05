/**
 * Function to update the content of a specific file.
 *
 * @param {Object} args - Arguments for the update.
 * @param {string} args.path - The path to the file to be updated.
 * @param {string} args.content - The updated content of the file.
 * @returns {Promise<Object>} - The result of the file update operation.
 */
const executeFunction = async ({ path, content }) => {
  const baseUrl = 'http://localhost:3000';
  const token = process.env.FUN_APIS_ONLY_API_KEY;
  
  try {
    // Construct the URL for the file update
    const url = `${baseUrl}/api/files/${encodeURIComponent(path)}`;

    // Set up headers for the request
    const headers = {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    };

    // Prepare the body of the request
    const body = JSON.stringify({ content });

    // Perform the fetch request
    const response = await fetch(url, {
      method: 'PUT',
      headers,
      body
    });

    // Check if the response was successful
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(JSON.stringify(errorData));
    }

    // Parse and return the response data
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error updating file:', error);
    return {
      error: `An error occurred while updating the file: ${error instanceof Error ? error.message : JSON.stringify(error)}`
    };
  }
};

/**
 * Tool configuration for updating a file.
 * @type {Object}
 */
const apiTool = {
  function: executeFunction,
  definition: {
    type: 'function',
    function: {
      name: 'update_file',
      description: 'Update the content of a specific file.',
      parameters: {
        type: 'object',
        properties: {
          path: {
            type: 'string',
            description: 'The path to the file to be updated.'
          },
          content: {
            type: 'string',
            description: 'The updated content of the file.'
          }
        },
        required: ['path', 'content']
      }
    }
  }
};

export { apiTool };
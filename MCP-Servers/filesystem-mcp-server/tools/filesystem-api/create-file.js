/**
 * Function to create a file on the server.
 *
 * @param {Object} args - Arguments for the file creation.
 * @param {string} args.path - The path where the file will be created.
 * @param {string} args.content - The content of the file to be created.
 * @returns {Promise<Object>} - The result of the file creation.
 */
const executeFunction = async ({ path, content }) => {
  const baseUrl = 'http://localhost:3000';
  const token = process.env.FUN_APIS_ONLY_API_KEY;

  try {
    // Construct the URL for the file creation
    const url = `${baseUrl}/api/files/${path}`;

    // Set up headers for the request
    const headers = {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    };

    // Create the request body
    const body = JSON.stringify({ content });

    // Perform the fetch request
    const response = await fetch(url, {
      method: 'POST',
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
    console.error('Error creating file:', error);
    return {
      error: `An error occurred while creating the file: ${error instanceof Error ? error.message : JSON.stringify(error)}`
    };
  }
};

/**
 * Tool configuration for creating a file on the server.
 * @type {Object}
 */
const apiTool = {
  function: executeFunction,
  definition: {
    type: 'function',
    function: {
      name: 'create_file',
      description: 'Create a file on the server.',
      parameters: {
        type: 'object',
        properties: {
          path: {
            type: 'string',
            description: 'The path where the file will be created.'
          },
          content: {
            type: 'string',
            description: 'The content of the file to be created.'
          }
        },
        required: ['path', 'content']
      }
    }
  }
};

export { apiTool };
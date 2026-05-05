/**
 * Function to create a directory in the filesystem API.
 *
 * @param {string} path - The path of the directory to create.
 * @returns {Promise<Object>} - The result of the directory creation.
 */
const createDirectory = async (path) => {
  const baseUrl = 'http://localhost:3000';
  const token = process.env.FUN_APIS_ONLY_API_KEY;
  try {
    // Construct the URL for the directory creation
    const url = `${baseUrl}/api/directories/${encodeURIComponent(path)}`;

    // Set up headers for the request
    const headers = {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    };

    // Perform the fetch request
    const response = await fetch(url, {
      method: 'POST',
      headers
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
    console.error('Error creating directory:', error);
    return {
      error: `An error occurred while creating the directory: ${error instanceof Error ? error.message : JSON.stringify(error)}`
    };
  }
};

/**
 * Tool configuration for creating a directory in the filesystem API.
 * @type {Object}
 */
const apiTool = {
  function: createDirectory,
  definition: {
    type: 'function',
    function: {
      name: 'create_directory',
      description: 'Create a new directory in the filesystem.',
      parameters: {
        type: 'object',
        properties: {
          path: {
            type: 'string',
            description: 'The path of the directory to create.'
          }
        },
        required: ['path']
      }
    }
  }
};

export { apiTool };
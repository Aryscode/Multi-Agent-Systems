/**
 * Function to list the contents of a directory using the Postman Filesystem API.
 *
 * @param {string} path - The path of the directory to list.
 * @returns {Promise<Object>} - The result of the directory listing.
 */
const executeFunction = async (path) => {
  const baseUrl = 'http://localhost:3000';
  const token = process.env.FUN_APIS_ONLY_API_KEY;
  try {
    // Construct the URL for the directory listing
    const url = `${baseUrl}/api/directories/${encodeURIComponent(path)}`;

    // Set up headers for the request
    const headers = {
      'Authorization': `Bearer ${token}`
    };

    // Perform the fetch request
    const response = await fetch(url, {
      method: 'GET',
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
    console.error('Error listing directory contents:', error);
    return {
      error: `An error occurred while listing directory contents: ${error instanceof Error ? error.message : JSON.stringify(error)}`
    };
  }
};

/**
 * Tool configuration for listing directory contents using the Postman Filesystem API.
 * @type {Object}
 */
const apiTool = {
  function: executeFunction,
  definition: {
    type: 'function',
    function: {
      name: 'list_directory_contents',
      description: 'List the contents of a directory.',
      parameters: {
        type: 'object',
        properties: {
          path: {
            type: 'string',
            description: 'The path of the directory to list.'
          }
        },
        required: ['path']
      }
    }
  }
};

export { apiTool };
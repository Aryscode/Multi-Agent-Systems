/**
 * Function to delete a directory in the filesystem.
 *
 * @param {Object} args - Arguments for the delete directory operation.
 * @param {string} args.path - The path of the directory to delete.
 * @returns {Promise<Object>} - The result of the delete operation.
 */
const executeFunction = async ({ path }) => {
  const baseUrl = 'http://localhost:3000';
  const token = process.env.FUN_APIS_ONLY_API_KEY;
  try {
    // Construct the URL for the delete request
    const url = `${baseUrl}/api/directories/${encodeURIComponent(path)}`;

    // Set up headers for the request
    const headers = {
      'Authorization': `Bearer ${token}`
    };

    // Perform the fetch request
    const response = await fetch(url, {
      method: 'DELETE',
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
    console.error('Error deleting directory:', error);
    return {
      error: `An error occurred while deleting the directory: ${error instanceof Error ? error.message : JSON.stringify(error)}`
    };
  }
};

/**
 * Tool configuration for deleting a directory in the filesystem.
 * @type {Object}
 */
const apiTool = {
  function: executeFunction,
  definition: {
    type: 'function',
    function: {
      name: 'delete_directory',
      description: 'Delete a directory in the filesystem.',
      parameters: {
        type: 'object',
        properties: {
          path: {
            type: 'string',
            description: 'The path of the directory to delete.'
          }
        },
        required: ['path']
      }
    }
  }
};

export { apiTool };
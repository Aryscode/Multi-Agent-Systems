/**
 * Function to read a file from the filesystem API.
 *
 * @param {string} path - The path of the file to read.
 * @returns {Promise<Object>} - The content of the file or an error message.
 */
const executeFunction = async (path) => {
  const baseUrl = 'http://localhost:3000';
  const token = process.env.FUN_APIS_ONLY_API_KEY;
  try {
    // Construct the URL for the file
    const url = `${baseUrl}/api/files/${encodeURIComponent(path)}`;

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
    const data = await response.text();
    return { content: data };
  } catch (error) {
    console.error('Error reading file:', error);
    return {
      error: `An error occurred while reading the file: ${error instanceof Error ? error.message : JSON.stringify(error)}`
    };
  }
};

/**
 * Tool configuration for reading a file from the filesystem API.
 * @type {Object}
 */
const apiTool = {
  function: executeFunction,
  definition: {
    type: 'function',
    function: {
      name: 'read_file',
      description: 'Read a file from the filesystem API.',
      parameters: {
        type: 'object',
        properties: {
          path: {
            type: 'string',
            description: 'The path of the file to read.'
          }
        },
        required: ['path']
      }
    }
  }
};

export { apiTool };
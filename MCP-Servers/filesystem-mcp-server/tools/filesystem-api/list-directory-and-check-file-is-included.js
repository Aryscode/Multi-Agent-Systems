/**
 * Function to list directory contents and check if a specific file is included.
 *
 * @param {Object} args - Arguments for the directory listing.
 * @param {string} args.directoryName - The name of the directory to list.
 * @param {string} args.fileName - The name of the file to check for in the directory.
 * @returns {Promise<Object>} - The result of the directory listing and file check.
 */
const executeFunction = async ({ directoryName, fileName }) => {
  const baseUrl = 'http://localhost:3000';
  const token = process.env.FUN_APIS_ONLY_API_KEY;
  try {
    // Set up the request URL
    const url = `${baseUrl}/api/directories/${directoryName}`;

    // Set up headers for the request
    const headers = {
      'Authorization': `Bearer ${token}`
    };

    // Perform the fetch request to list directory contents
    const response = await fetch(url, {
      method: 'GET',
      headers
    });

    // Check if the response was successful
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(JSON.stringify(errorData));
    }

    // Parse the response data
    const data = await response.json();

    // Check if the specified file is included in the directory contents
    const foundFile = data.find(item => item.name === fileName && !item.isDirectory);
    
    return {
      directoryContents: data,
      fileExists: !!foundFile
    };
  } catch (error) {
    console.error('Error listing directory contents:', error);
    return {
      error: `An error occurred while listing directory contents: ${error instanceof Error ? error.message : JSON.stringify(error)}`
    };
  }
};

/**
 * Tool configuration for listing directory contents and checking for a file.
 * @type {Object}
 */
const apiTool = {
  function: executeFunction,
  definition: {
    type: 'function',
    function: {
      name: 'list_directory_and_check_file',
      description: 'List directory contents and check if a specific file is included.',
      parameters: {
        type: 'object',
        properties: {
          directoryName: {
            type: 'string',
            description: 'The name of the directory to list.'
          },
          fileName: {
            type: 'string',
            description: 'The name of the file to check for in the directory.'
          }
        },
        required: ['directoryName', 'fileName']
      }
    }
  }
};

export { apiTool };
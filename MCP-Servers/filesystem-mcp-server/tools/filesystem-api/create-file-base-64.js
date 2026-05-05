/**
 * Function to create a file using Base64 encoded data.
 *
 * @param {Object} args - Arguments for the file creation.
 * @param {string} args.fileData - The Base64 encoded data of the file.
 * @param {string} [args.path='file-base64.txt'] - The path where the file will be created.
 * @returns {Promise<Object>} - The result of the file creation.
 */
const executeFunction = async ({ fileData, path = 'file-base64.txt' }) => {
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

    // Prepare the body for the request
    const body = JSON.stringify({ fileData });

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
 * Tool configuration for creating a file using Base64 encoded data.
 * @type {Object}
 */
const apiTool = {
  function: executeFunction,
  definition: {
    type: 'function',
    function: {
      name: 'create_file_base64',
      description: 'Create a file using Base64 encoded data.',
      parameters: {
        type: 'object',
        properties: {
          fileData: {
            type: 'string',
            description: 'The Base64 encoded data of the file.'
          },
          path: {
            type: 'string',
            description: 'The path where the file will be created.'
          }
        },
        required: ['fileData']
      }
    }
  }
};

export { apiTool };
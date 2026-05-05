/**
 * Function to upload a file to the Postman Filesystem API.
 *
 * @param {Object} args - Arguments for the file upload.
 * @param {string} args.path - The path where the file will be uploaded.
 * @param {string} args.file - The file to be uploaded.
 * @returns {Promise<Object>} - The result of the file upload.
 */
const executeFunction = async ({ path, file }) => {
  const baseUrl = 'http://localhost:3000';
  const token = process.env.FUN_APIS_ONLY_API_KEY;

  try {
    const formData = new FormData();
    formData.append('file', file);

    // Set up headers for the request
    const headers = {
      'Authorization': `Bearer ${token}`
    };

    // Perform the fetch request
    const response = await fetch(`${baseUrl}/api/files/${path}`, {
      method: 'POST',
      headers,
      body: formData
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
    console.error('Error uploading file:', error);
    return {
      error: `An error occurred while uploading the file: ${error instanceof Error ? error.message : JSON.stringify(error)}`
    };
  }
};

/**
 * Tool configuration for uploading a file to the Postman Filesystem API.
 * @type {Object}
 */
const apiTool = {
  function: executeFunction,
  definition: {
    type: 'function',
    function: {
      name: 'upload_file',
      description: 'Upload a file to the Postman Filesystem API.',
      parameters: {
        type: 'object',
        properties: {
          path: {
            type: 'string',
            description: 'The path where the file will be uploaded.'
          },
          file: {
            type: 'string',
            description: 'The file to be uploaded.'
          }
        },
        required: ['path', 'file']
      }
    }
  }
};

export { apiTool };
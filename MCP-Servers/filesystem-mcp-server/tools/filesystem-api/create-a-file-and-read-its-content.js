/**
 * Function to create a file and read its content using the Filesystem API.
 *
 * @param {Object} args - Arguments for the file operation.
 * @param {string} args.fileName - The name of the file to create.
 * @param {string} args.content - The content to write to the file.
 * @returns {Promise<Object>} - The response from the API after creating and reading the file.
 */
const executeFunction = async ({ fileName, content }) => {
  const baseUrl = 'http://localhost:3000';
  const token = process.env.FUN_APIS_ONLY_API_KEY;

  try {
    // Create the file
    const createResponse = await fetch(`${baseUrl}/api/files/${fileName}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ content })
    });

    if (!createResponse.ok) {
      const errorData = await createResponse.json();
      throw new Error(`Create file failed: ${errorData.error}`);
    }

    // Read the file content
    const readResponse = await fetch(`${baseUrl}/api/files/${fileName}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!readResponse.ok) {
      const errorData = await readResponse.json();
      throw new Error(`Read file failed: ${errorData.error}`);
    }

    const fileContent = await readResponse.text();
    return { fileName, content: fileContent };
  } catch (error) {
    console.error('Error creating and reading file:', error);
    return {
      error: `An error occurred while creating and reading the file: ${error instanceof Error ? error.message : JSON.stringify(error)}`
    };
  }
};

/**
 * Tool configuration for creating a file and reading its content using the Filesystem API.
 * @type {Object}
 */
const apiTool = {
  function: executeFunction,
  definition: {
    type: 'function',
    function: {
      name: 'create_and_read_file',
      description: 'Create a file and read its content using the Filesystem API.',
      parameters: {
        type: 'object',
        properties: {
          fileName: {
            type: 'string',
            description: 'The name of the file to create.'
          },
          content: {
            type: 'string',
            description: 'The content to write to the file.'
          }
        },
        required: ['fileName', 'content']
      }
    }
  }
};

export { apiTool };
/**
 * Function to set up authentication token for the Postman Filesystem API.
 *
 * @param {Object} args - Arguments for the setup.
 * @param {string} args.token - The token used for authentication setup.
 * @returns {Promise<Object>} - The result of the authentication setup.
 */
const executeFunction = async ({ token }) => {
  const baseUrl = 'http://localhost:3000';
  const authToken = ''; // will be provided by the user
  try {
    // Construct the URL for the setup token
    const url = `${baseUrl}/api/auth/setup`;

    // Set up headers for the request
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authToken}`
    };

    // Prepare the request body
    const body = JSON.stringify({ token });

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
    console.error('Error setting up token:', error);
    return {
      error: `An error occurred while setting up the token: ${error instanceof Error ? error.message : JSON.stringify(error)}`
    };
  }
};

/**
 * Tool configuration for setting up authentication token for the Postman Filesystem API.
 * @type {Object}
 */
const apiTool = {
  function: executeFunction,
  definition: {
    type: 'function',
    function: {
      name: 'setup_token',
      description: 'Set up authentication token for the Postman Filesystem API.',
      parameters: {
        type: 'object',
        properties: {
          token: {
            type: 'string',
            description: 'The token used for authentication setup.'
          }
        },
        required: ['token']
      }
    }
  }
};

export { apiTool };
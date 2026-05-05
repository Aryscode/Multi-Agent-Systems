/**
 * Function to upload a file to a specified directory and delete both the file and directory afterwards.
 *
 * @param {Object} args - Arguments for the file upload and deletion.
 * @param {string} args.filePath - The path of the file to upload.
 * @param {string} args.fileName - The name of the file to be uploaded.
 * @param {string} args.directoryName - The name of the directory where the file will be uploaded.
 * @returns {Promise<Object>} - The result of the upload and deletion process.
 */
const executeFunction = async ({ filePath, fileName, directoryName }) => {
  const baseUrl = 'http://localhost:3000';
  const token = process.env.FUN_APIS_ONLY_API_KEY;

  try {
    // Construct the URL with query parameters
    const url = new URL(`${baseUrl}/api/files/${directoryName ? `${directoryName}/${fileName}` : fileName}`);
    const formData = new FormData();
    formData.append('file', fs.createReadStream(filePath));

    // Set up headers for the request
    const headers = {
      'Authorization': `Bearer ${token}`
    };

    // Perform the fetch request to upload the file
    const response = await fetch(url.toString(), {
      method: 'POST',
      headers,
      body: formData
    });

    // Check if the response was successful
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(JSON.stringify(errorData));
    }

    // Read back the uploaded file to verify its contents
    const uploadedContent = await fetch(url.toString(), {
      method: 'GET',
      headers
    });

    if (!uploadedContent.ok) {
      throw new Error('Failed to read back the uploaded file.');
    }

    const content = await uploadedContent.text();
    console.log(`Uploaded file size: ${content.length} bytes`);

    // Now delete the file
    const deleteResponse = await fetch(url.toString(), {
      method: 'DELETE',
      headers
    });

    if (!deleteResponse.ok) {
      const deleteErrorData = await deleteResponse.json();
      throw new Error(JSON.stringify(deleteErrorData));
    }

    // If a directory was specified, delete it
    if (directoryName) {
      const deleteDirResponse = await fetch(`${baseUrl}/api/directories/${directoryName}`, {
        method: 'DELETE',
        headers
      });

      if (!deleteDirResponse.ok) {
        const deleteDirErrorData = await deleteDirResponse.json();
        throw new Error(JSON.stringify(deleteDirErrorData));
      }
    }

    return { message: 'File uploaded and deleted successfully.' };
  } catch (error) {
    console.error('Error during file upload and deletion:', error);
    return {
      error: `An error occurred: ${error instanceof Error ? error.message : JSON.stringify(error)}`
    };
  }
};

/**
 * Tool configuration for uploading and deleting files in a filesystem API.
 * @type {Object}
 */
const apiTool = {
  function: executeFunction,
  definition: {
    type: 'function',
    function: {
      name: 'upload_and_delete_file',
      description: 'Upload a file to a specified directory and delete both the file and directory afterwards.',
      parameters: {
        type: 'object',
        properties: {
          filePath: {
            type: 'string',
            description: 'The path of the file to upload.'
          },
          fileName: {
            type: 'string',
            description: 'The name of the file to be uploaded.'
          },
          directoryName: {
            type: 'string',
            description: 'The name of the directory where the file will be uploaded.'
          }
        },
        required: ['filePath', 'fileName']
      }
    }
  }
};

export { apiTool };
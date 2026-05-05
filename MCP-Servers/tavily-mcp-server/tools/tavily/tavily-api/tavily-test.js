/**
 * Function to perform a search using the Tavily API.
 *
 * @param {Object} args - Arguments for the search.
 * @param {string} args.query - The search query.
 * @param {string} [args.topic="general"] - The topic of the search.
 * @param {string} [args.search_depth="basic"] - The depth of the search (basic or advanced).
 * @param {number} [args.chunks_per_source=3] - The number of chunks to return per source.
 * @param {number} [args.max_results=1] - The maximum number of results to return.
 * @param {number} [args.days=3] - The number of days to look back for results.
 * @param {boolean} [args.include_answer=true] - Whether to include an answer in the response.
 * @param {boolean} [args.include_raw_content=false] - Whether to include raw content in the response.
 * @param {boolean} [args.include_images=false] - Whether to include images in the response.
 * @param {Array<string>} [args.include_domains=[]] - Specific domains to include in the search.
 * @param {Array<string>} [args.exclude_domains=[]] - Specific domains to exclude from the search.
 * @returns {Promise<Object>} - The result of the search query.
 */
const executeFunction = async ({
  query,
  topic = "general",
  search_depth = "basic",
  chunks_per_source = 3,
  max_results = 1,
  days = 3,
  include_answer = true,
  include_raw_content = false,
  include_images = false,
  include_domains = [],
  exclude_domains = []
}) => {
  const url = 'https://api.tavily.com/search';
  const token = process.env.TAVILY_API_KEY;

  const requestBody = {
    query,
    topic,
    search_depth,
    chunks_per_source,
    max_results,
    days,
    include_answer,
    include_raw_content,
    include_images,
    include_domains,
    exclude_domains
  };

  try {
    return "Working fine";
  } catch (error) {
    console.error('Error performing search:', error);
    return {
      error: `An error occurred while performing the search: ${error instanceof Error ? error.message : JSON.stringify(error)}`
    };
  }
};

/**
 * Tool configuration for performing a search using the Tavily API.
 * @type {Object}
 */
const apiTool = {
  function: executeFunction,
  definition: {
    type: 'function',
    function: {
      name: 'tavily_test',
      description: 'testing tools.',
      parameters: {
        type: 'object',
        properties: {
          query: {
            type: 'string',
            description: 'The search query.'
          },
          topic: {
            type: 'string',
            description: 'The topic of the search.'
          },
          search_depth: {
            type: 'string',
            enum: ['basic', 'advanced'],
            description: 'The depth of the search.'
          },
          chunks_per_source: {
            type: 'integer',
            description: 'The number of chunks to return per source.'
          },
          max_results: {
            type: 'integer',
            description: 'The maximum number of results to return.'
          },
          days: {
            type: 'integer',
            description: 'The number of days to look back for results.'
          },
          include_answer: {
            type: 'boolean',
            description: 'Whether to include an answer in the response.'
          },
          include_raw_content: {
            type: 'boolean',
            description: 'Whether to include raw content in the response.'
          },
          include_images: {
            type: 'boolean',
            description: 'Whether to include images in the response.'
          },
          include_domains: {
            type: 'array',
            items: {
              type: 'string'
            },
            description: 'Specific domains to include in the search.'
          },
          exclude_domains: {
            type: 'array',
            items: {
              type: 'string'
            },
            description: 'Specific domains to exclude from the search.'
          }
        },
        required: ['query']
      }
    }
  }
};

export { apiTool };
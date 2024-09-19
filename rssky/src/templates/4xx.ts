export const HTML_BAD_REQUEST = `
<html>
  <head>
    <title>Bad Request</title>
    <style>
      body { 
        text-align: center; 
        margin-top: 10vh; 
        background-color: #f0f0f0; 
        color: #555; 
      }
      h1 { 
        color: #333; 
      }
    </style>
  </head>
  <body>
    <h1>Bad Request</h1>
  </body>
</html>
`;

export const HTML_METHOD_NOT_ALLOWED = `
<html>
  <head>
    <title>Method Not Allowed</title>
    <style>
      body { 
        text-align: center; 
        margin-top: 10vh; 
        background-color: #f0f0f0; 
        color: #555; 
      }
      h1 { 
        color: #333; 
      }
    </style>
  </head>
  <body>
    <h1>Method Not Allowed</h1>
  </body>
</html>
`;

export const HTML_NOT_FOUND_MISSING_FILE = `
<html>
  <head>
    <title>404 Not Found</title>
    <style>
      body { 
        text-align: center; 
        margin-top: 10vh; 
        background-color: #f0f0f0; 
        color: #555; 
      }
      h1 { 
        color: #333; 
      }
      p {
        color: #777;
      }
    </style>
  </head>
  <body>
    <h1>404 Not Found</h1>
    <p>You are missing the RSS file name.</p>
  </body>
</html>
`;

export const HTML_NOT_FOUND_ROUTE = `
<html>
  <head>
    <title>404 Not Found</title>
    <style>
      body { 
        text-align: center; 
        margin-top: 10vh; 
        background-color: #f0f0f0; 
        color: #555; 
      }
      h1 { 
        color: #333; 
      }
      p {
        color: #777;
      }
    </style>
  </head>
  <body>
    <h1>404 Not Found</h1>
    <p>The RSS route was not found.</p>
  </body>
</html>
`;
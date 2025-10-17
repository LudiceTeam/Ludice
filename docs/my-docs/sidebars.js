// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  docsSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: 'Introduction',
    },
    {
      type: 'category',
      label: 'Getting Started',
      items: [
        'setup-guide',
      ],
    },
    {
      type: 'category',
      label: 'Technical Documentation',
      items: [
        'technical-architecture',
        'api-documentation',
        'development-guide',
      ],
    },
    {
      type: 'category',
      label: 'Legal',
      items: [
        'legal/BOT_SUMMARY',
        'legal/TERMS_OF_SERVICE',
        'legal/PRIVACY_POLICY',
        'legal/RESPONSIBLE_GAMBLING',
        'legal/README',
      ],
    },
  ],
};

export default sidebars;

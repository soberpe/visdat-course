// @ts-check
const remarkMath = require('remark-math').default || require('remark-math');
const rehypeKatex = require('rehype-katex').default || require('rehype-katex');

const config = {
  title: 'Visualisierung & Datenaufbereitung',
  tagline: 'VIS3VO Course Materials',
  url: 'https://soberpe.github.io',
  baseUrl: '/visdat-course/',
  onBrokenLinks: 'throw',
  organizationName: 'soberpe',
  projectName: 'visdat-course',
  deploymentBranch: 'gh-pages',
  trailingSlash: false,
  markdown: {
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },
  themes: ['@docusaurus/theme-mermaid'],
  presets: [
    ['@docusaurus/preset-classic', {
      docs: { 
        routeBasePath: '/', 
        sidebarPath: require.resolve('./sidebars.js'),
        editUrl: 'https://github.com/soberpe/visdat-course/tree/main/',
        remarkPlugins: [remarkMath],
        rehypePlugins: [rehypeKatex],
      },
      blog: false, 
      theme: { 
        customCss: require.resolve('./src/css/custom.css')
      }
    }]
  ],
  themeConfig: {
    colorMode: {
      respectPrefersColorScheme: true,
    },
    mermaid: {
      theme: { light: 'neutral', dark: 'dark' },
      options: {
        fontFamily: "'IBM Plex Sans', system-ui, sans-serif",
        fontSize: 15,
        flowchart: { padding: 14, nodeSpacing: 45, rankSpacing: 60 },
      },
    },
    navbar: {
      title: 'VIS3VO',
      items: [
        {
          href: 'https://github.com/soberpe/visdat-course',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      copyright: `Copyright © ${new Date().getFullYear()} Stefan Oberpeilsteiner. Built with Docusaurus.`,
    },
  },
  stylesheets: [
    {
      href: 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap',
      type: 'text/css',
    },
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.13.24/dist/katex.min.css',
      type: 'text/css',
      integrity: 'sha384-odtC+0UGzzFL/6PNoE8rX/SPcQDXBJ+uRepguP4QkPCm2LBxH3FA3y+fKSiJ+AmM',
      crossorigin: 'anonymous',
    },
  ],
};
module.exports = config;

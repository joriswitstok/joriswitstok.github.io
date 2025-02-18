import path from 'path';
import { fileURLToPath } from 'url';

import { defineConfig } from 'astro/config';

import sitemap from '@astrojs/sitemap';
import tailwind from '@astrojs/tailwind';
import mdx from '@astrojs/mdx';
import partytown from '@astrojs/partytown';
import icon from 'astro-icon';
import compress from 'astro-compress';
import type { AstroIntegration } from 'astro';

import astrowind from './vendor/integration';

import { readingTimeRemarkPlugin, responsiveTablesRehypePlugin, lazyImagesRehypePlugin } from './src/utils/frontmatter';

import cookieconsent from "@jop-software/astro-cookieconsent";
const __dirname = path.dirname(fileURLToPath(import.meta.url));

const hasExternalScripts = false;
const whenExternalScripts = (items: (() => AstroIntegration) | (() => AstroIntegration)[] = []) =>
  hasExternalScripts ? (Array.isArray(items) ? items.map((item) => item()) : [items()]) : [];

export default defineConfig({
  output: 'static',

  integrations: [
    cookieconsent({
      guiOptions: {
          consentModal: {
              layout: "box",
              position: "bottom left",
              equalWeightButtons: true,
              flipButtons: false
          },
          preferencesModal: {
              layout: "box",
              position: "right",
              equalWeightButtons: true,
              flipButtons: false
          }
      },
      categories: {
          necessary: {
              readOnly: true
          },
          analytics: {}
      },
      language: {
          default: "en",
          autoDetect: "browser",
          translations: {
              en: {
                  consentModal: {
                      title: "Hello traveller, it's cookie time!",
                      description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip.",
                      acceptAllBtn: "Accept all",
                      acceptNecessaryBtn: "Reject all",
                      showPreferencesBtn: "Manage preferences",
                      footer: "<a href=\"#link\">Privacy Policy</a>\n<a href=\"#link\">Terms and conditions</a>"
                  },
                  preferencesModal: {
                      title: "Consent Preferences Center",
                      acceptAllBtn: "Accept all",
                      acceptNecessaryBtn: "Reject all",
                      savePreferencesBtn: "Save preferences",
                      closeIconLabel: "Close modal",
                      serviceCounterLabel: "Service|Services",
                      sections: [
                          {
                              title: "Cookie Usage",
                              description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
                          },
                          {
                              title: "Strictly Necessary Cookies <span class=\"pm__badge\">Always Enabled</span>",
                              description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
                              linkedCategory: "necessary"
                          },
                          {
                              title: "Analytics Cookies",
                              description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
                              linkedCategory: "analytics"
                          },
                          {
                              title: "More information",
                              description: "For any query in relation to my policy on cookies and your choices, please <a class=\"cc__link\" href=\"#yourdomain.com\">contact me</a>."
                          }
                      ]
                  }
              }
          }
      }
    }),
    tailwind({
      applyBaseStyles: false,
    }),
    sitemap(),
    mdx(),
    icon({
      include: {
        tabler: ['*'],
        mdi: ["*"],
        'flat-color-icons': [
          'template',
          'gallery',
          'approval',
          'document',
          'advertising',
          'currency-exchange',
          'voice-presentation',
          'business-contact',
          'database',
        ],
      },
    }),

    ...whenExternalScripts(() =>
      partytown({
        config: { forward: ['dataLayer.push'] },
      })
    ),

    compress({
      CSS: true,
      HTML: {
        'html-minifier-terser': {
          removeAttributeQuotes: false,
        },
      },
      Image: false,
      JavaScript: true,
      SVG: false,
      Logger: 1,
    }),

    astrowind({
      config: './src/config.yaml',
    }),
  ],

  image: {
    domains: ['cdn.pixabay.com'],
  },

  markdown: {
    remarkPlugins: [readingTimeRemarkPlugin],
    rehypePlugins: [responsiveTablesRehypePlugin, lazyImagesRehypePlugin],
  },

  vite: {
    resolve: {
      alias: {
        '~': path.resolve(__dirname, './src'),
      },
    },
  },
});

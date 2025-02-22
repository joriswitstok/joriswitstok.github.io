
import { getPermalink, getHomePermalink } from './utils/permalinks';
const currentYear = new Date().getFullYear();

export const headerData = {
  links: [
    {
      text: 'Home',
      href: getHomePermalink(),
    },
    {
      text: 'About',
      href: getPermalink('/about'),
      links: [
        {
          text: 'CV',
          href: getPermalink('/about/cv'),
        },
        {
          text: 'Publications',
          href: getPermalink('/about/publications'),
        },
      ]
    },
    {
      text: 'Science',
      href: getPermalink('/science'),
      links: [
        {
          text: 'For Public',
          href: getPermalink('/science/public'),
        },
        {
          text: 'For Scientists',
          href: getPermalink('/science/research'),
        },
      ],
    },
    {
      text: 'News',
      href: getPermalink('/news'),
    },
  ],
  actions: [{ text: 'GitHub', href: 'https://github.com/joriswitstok', target: '_blank' }],
};

export const footerData = {
  links: [
    {
      title: 'Main',
      href: getHomePermalink(),
      links: [
        { text: 'About', href: getPermalink('/about') },
        { text: 'CV', href: getPermalink('/about/cv') },
        { text: 'Publications', href: getPermalink('/about/publications') },
      ],
    },
    {
      title: 'Science',
      href: getPermalink('/science'),
      links: [
        {
          text: 'For Public',
          href: getPermalink('/science/public'),
        },
        {
          text: 'For Scientists',
          href: getPermalink('/science/research'),
        },
        {
          text: 'News & Media',
          href: getPermalink('/news'),
        },
      ],
    },
    {
      title: 'Affiliations',
      links: [
        { text: 'Cosmic Dawn Center', href: 'https://cosmicdawn.dk', target: '_blank' },
        { text: 'Niels Bohr Institute', href: 'https://nbi.ku.dk/english/', target: '_blank' },
        { text: 'JADES Collaboration', href: 'https://jades-survey.github.io', target: '_blank' },
      ],
    },
    {
      title: 'Observatories',
      links: [
        { text: 'JWST', href: 'https://www.stsci.edu/jwst/', target: '_blank' },
        { text: 'ALMA', href: 'https://almascience.eso.org', target: '_blank' },
        { text: 'ESO', href: 'https://www.eso.org/sci.html', target: '_blank' },
      ],
    },
  ],
  secondaryLinks: [
    { text: 'Privacy Policy', href: getPermalink('/privacy') },
  ],
  socialLinks: [
    { ariaLabel: 'Github', icon: 'tabler:brand-github', href: 'https://github.com/joriswitstok', target: '_blank' },
    { ariaLabel: 'BlueSky', icon: 'tabler:brand-bluesky', href: 'https://bsky.app/profile/joriswitstok.bsky.social', target: '_blank' },
  ],
  footNote: `
    © ${currentYear} <a href=${getHomePermalink()}> Joris Witstok </a> · <a href="https://github.com/onwidget/astrowind/blob/main/LICENSE.md" target="_blank"> All rights reserved</a>.
  `,
};

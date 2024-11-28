
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
        {
          text: 'News & Media',
          href: getPermalink('/science/news'),
        },
      ],
    },
    {
      text: 'CV',
      href: getPermalink('/cv'),
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
        { text: 'CV', href: getPermalink('/cv') },
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
          href: getPermalink('/science/news'),
        },
      ],
    },
    {
      title: 'External',
      links: [
        { text: 'Cosmic Dawn Center', href: 'https://cosmicdawn.dk', target: '_blank' },
        { text: 'JADES Collaboration', href: 'https://jades-survey.github.io', target: '_blank' },
        { text: 'Kavli Institute for Cosmology', href: 'https://www.kicc.cam.ac.uk', target: '_blank' },
        { text: 'Cavendish Astrophysics', href: 'https://www.astro.phy.cam.ac.uk', target: '_blank' },
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

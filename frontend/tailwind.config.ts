import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // SOA primary blue scale — anchored on #00538e (SOA brand blue)
        primary: {
          50:  '#eaf3fa',  // pill-blue background
          100: '#d0e6f4',
          200: '#a1ceea',
          300: '#72b5df',
          400: '#439dd5',
          500: '#196499',  // hover state
          600: '#00538e',  // SOA brand primary
          700: '#004272',  // active / pressed
          800: '#023153',  // deep navy — link hover
          900: '#0d1c27',  // darkest navy — body text, footer
        },
        // SOA accent yellow — #ffd84e (registration box accent, CTA cards)
        accent: {
          50:  '#fffae7',
          100: '#fff3c4',
          200: '#ffe58a',
          300: '#ffd84e',  // SOA accent yellow (primary use)
          400: '#ffc820',
          500: '#f0b000',
          600: '#c88d00',
          700: '#a06c00',
          800: '#784d00',
          900: '#3e2500',
        },
        // SOA success / lime green — #a5c800
        success: {
          50:  '#f6fbde',
          100: '#eaf5b0',
          200: '#d5ec6a',
          300: '#c0e22e',
          400: '#a5c800',  // SOA lime/checkmark green
          500: '#88a600',
          600: '#6b8400',
          700: '#506200',
          800: '#364100',
          900: '#1c2100',
        },
        // SOA error red — #c71d28
        error: {
          50:  '#fef2f2',
          100: '#fedfde',  // SOA pill-red background
          200: '#fdbfbd',
          300: '#fa8f8c',
          400: '#f05f5b',
          500: '#e03035',
          600: '#c71d28',  // SOA red — banner buttons, error states
          700: '#a51521',
          800: '#83101a',
          900: '#550300',  // SOA pill-red text
        },
        // SOA teal — #74cbc8 (progress indicators, accents)
        teal: {
          50:  '#effafa',
          100: '#d5f2f1',
          200: '#aae5e4',
          300: '#74cbc8',  // SOA teal accent
          400: '#40b8b4',
          500: '#2a9a96',
          600: '#1e7d7a',
          700: '#15605d',
          800: '#0d4341',
          900: '#062625',
        },
        // SOA purple — #8e88f1 (CTA card accent)
        purple: {
          50:  '#f0effd',
          100: '#edecfa',  // SOA pill-purple background
          200: '#d6d4f6',
          300: '#b8b4f0',
          400: '#a39eeb',
          500: '#8e88f1',  // SOA purple accent
          600: '#6b63e0',
          700: '#4a41c8',
          800: '#2e28a0',
          900: '#09034c',  // SOA pill-purple text / btn-purple bg
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};

export default config;

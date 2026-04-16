// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  devServer: {
    port: 3000,
  },

  modules: [
    '@pinia/nuxt',
    '@nuxt/ui',
  ],

  css: ['~/assets/css/main.css'],
  
  // Nuxt UI v4 handles Tailwind v4 internally — no postcss or tailwind plugin needed
  app: {
    head: {
      title: 'Entity Canvas',
      htmlAttrs: { lang: 'en' },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content:
            'Entity Canvas — the modern workspace for database schema exploration and visual query building.',
        },
      ],
      link: [
        {
          rel: 'preconnect',
          href: 'https://fonts.googleapis.com',
        },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap',
        },
      ],
    },
  },

  runtimeConfig: {
    // Private: used on server-side only (merged with NUXT_API_BASE)
    apiBase: process.env.NUXT_API_BASE || 'http://backend:8080',
    public: {
      // Public: used on both client and server (merged with NUXT_PUBLIC_API_BASE)
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000',
    },
  },
})

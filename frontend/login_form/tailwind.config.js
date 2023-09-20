/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./src/*.html",
        "./node_modules/flowbite/**/*.js"
    ],
    theme: {
        minHeight: {
            '12': '3rem'
        },
        extend: {
            fontSize: {
                form: 'calc(20px + 10 * (100vw - 320px) / 1600)',
                header: 'calc(18px + 14 * (100vw - 320px) / 1600)',
                chart: 'calc(16px + 8 * (100vw - 320px) / 1600)'
            },
            colors: {
                primary: {
                    "50": "#eff6ff",
                    "100": "#dbeafe",
                    "200": "#bfdbfe",
                    "300": "#93c5fd",
                    "400": "#60a5fa",
                    "500": "#3b82f6",
                    "600": "#2563eb",
                    "700": "#1d4ed8",
                    "800": "#1e40af",
                    "900": "#1e3a8a"
                },
                'header-color': '#454D56',
                'button-color': '#23629F',
                'all-header-color': '#454D56',
                'eee': '#EEEEEE',
                'add-user-bg': 'rgba(255, 255, 255, 0.6)',
                'table-color': 'rgba(69, 77, 86, 0.15)',
            },
            backgroundImage: {
                'body-gradient': 'linear-gradient(90.23deg, #DED6C4 13.97%, #6897B6 99.28%)',
                'active-button-grad': 'linear-gradient(89.88deg, rgba(149, 175, 188, 1) 1.68%, rgba(130, 165, 185, 1) 99.89%)',
            },
            dropShadow: {
                'login-shadow': '0px 6px 4px rgba(0, 0, 0, 0.54)',
            },
            flex: {
                'footer': '0 0 auto;'
            },
        },
        fontFamily: {
            'body': [
                'Inter',
                'ui-sans-serif',
                'system-ui',
                '-apple-system',
                'system-ui',
                'Segoe UI',
                'Roboto',
                'Helvetica Neue',
                'Arial',
                'Noto Sans',
                'sans-serif',
                'Apple Color Emoji',
                'Segoe UI Emoji',
                'Segoe UI Symbol',
                'Noto Color Emoji'
            ],
            'sans': [
                'Inter',
                'ui-sans-serif',
                'system-ui',
                '-apple-system',
                'system-ui',
                'Segoe UI',
                'Roboto',
                'Helvetica Neue',
                'Arial',
                'Noto Sans',
                'sans-serif',
                'Apple Color Emoji',
                'Segoe UI Emoji',
                'Segoe UI Symbol',
                'Noto Color Emoji'
            ],
            // 'montserrat': "'Montserrat', sans-serif",
            'montserrat': '\'Montserrat\', sans-serif'
        }
    },
    plugins: [
        require('flowbite/plugin'),
        require('tailwind-scrollbar')
    ],
}

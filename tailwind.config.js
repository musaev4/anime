/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/**/*.html",
        "./static/**/*.js",
        "./**/forms.py",
        "./**/views.py"
    ],
    theme: {
        extend: {
            colors: {
                // Ваши кастомные цвета
            },
        },
    },
    plugins: [
        require('tailwind-scrollbar'),
    ],
}
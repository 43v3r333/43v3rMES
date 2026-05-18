import { ref, watch, onMounted } from 'vue'

export function useDarkMode() {
  const isDark = ref(localStorage.getItem('theme') === 'dark')

  const toggleDark = () => {
    isDark.value = !isDark.value
    localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
  }

  watch(isDark, (val) => {
    if (val) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, { immediate: true })

  return { isDark, toggleDark }
}

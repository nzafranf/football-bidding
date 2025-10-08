function showToast(title, message, type = 'normal', duration = 3000) {
    const toastComponent = document.getElementById('toast-component');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');
    const toastIcon = document.getElementById('toast-icon');

    if (!toastComponent) return;

    // show container
    toastComponent.style.display = 'flex';

    // reset classes/styles
    toastComponent.classList.remove(
        'bg-red-50', 'border-red-500', 'text-red-600',
        'bg-green-50', 'border-green-500', 'text-green-600',
        'bg-white', 'border-gray-300', 'text-gray-800'
    );
    toastComponent.style.border = '';

    // type-specific icon & style
    if (type === 'success') {
        toastIcon.textContent = '✔️';
        toastComponent.classList.add('bg-magenta-900', 'border-magenta-500', 'text-magenta-300');
        toastComponent.style.border = '1px solid #ff00ff';
    } else if (type === 'error') {
        toastIcon.textContent = '❌';
        toastComponent.classList.add('bg-red-900', 'border-red-500', 'text-red-300');
        toastComponent.style.border = '1px solid #ef4444';
    } else {
        toastIcon.textContent = 'ℹ️';
        toastComponent.classList.add('bg-black', 'border-magenta-500', 'text-white');
        toastComponent.style.border = '1px solid #ff00ff';
    }

    toastTitle.textContent = title || '';
    toastMessage.textContent = message || '';

    // animate in
    toastComponent.classList.remove('opacity-0', 'translate-y-64');
    toastComponent.classList.add('opacity-100', 'translate-y-0');

    // cancel previous hide timer
    if (toastComponent._hideTimeout) {
        clearTimeout(toastComponent._hideTimeout);
    }

    toastComponent._hideTimeout = setTimeout(() => {
        toastComponent.classList.remove('opacity-100', 'translate-y-0');
        toastComponent.classList.add('opacity-0', 'translate-y-64');

        // hide after animation ends (300ms)
        setTimeout(() => {
            toastComponent.style.display = 'none';
        }, 300);
    }, duration);
}

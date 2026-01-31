document.addEventListener('DOMContentLoaded', function () {

    const csrfTokenEl = document.querySelector('[name="csrfmiddlewaretoken"]');
    if (!csrfTokenEl) return;

    const csrfToken = csrfTokenEl.value;

    function findCaptchaElements() {
        return {
            captchaImg: document.querySelector('img[src*="captcha"], img.captcha, .captcha img'),
            captchaKey: document.querySelector('input[name="captcha_0"], #id_captcha_0'),
            captchaInput: document.querySelector('input[name="captcha_1"], #id_captcha_1'),
            submitBtn: document.getElementById('submitBtn'),
            refreshBtn: document.getElementById('refreshBtn') || document.getElementById('refreshLink')
        };
    }

    const elements = findCaptchaElements();
    if (!elements.submitBtn || !elements.captchaInput) return;

    /* ===== DISABLE SUBMIT INITIALLY ===== */
    elements.submitBtn.disabled = !elements.captchaInput.value.trim();

    /* ===== ENABLE SUBMIT ON CAPTCHA INPUT ===== */
    elements.captchaInput.addEventListener('input', function () {
        elements.submitBtn.disabled = !this.value.trim();
    });

    /* ===== REFRESH CAPTCHA ===== */
    function refreshCaptcha() {
        const el = findCaptchaElements();
        if (!el.captchaImg || !el.captchaKey) return;

        if (el.refreshBtn) {
            el.refreshBtn.classList.add('refreshing');
            el.refreshBtn.textContent = '🔄 Refreshing...';
        }

        fetch('/captcha/refresh/', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            }
        })
        .then(res => res.json())
        .then(data => {
            el.captchaImg.src = data.image_url + '?t=' + new Date().getTime();
            el.captchaKey.value = data.key;
            el.captchaInput.value = '';
            el.submitBtn.disabled = true;
        })
        .finally(() => {
            if (el.refreshBtn) {
                el.refreshBtn.classList.remove('refreshing');
                el.refreshBtn.textContent = '🔄 Refresh Captcha';
            }
        });
    }

    /* ===== BIND REFRESH BUTTON ===== */
    if (elements.refreshBtn) {
        elements.refreshBtn.addEventListener('click', function (e) {
            e.preventDefault();
            refreshCaptcha();
        });
    }

    /* ===== AUTO REFRESH ON ERROR ===== */
    if (document.querySelector('.error')) {
        setTimeout(refreshCaptcha, 500);
    }

});

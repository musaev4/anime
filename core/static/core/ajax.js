function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function deleteImage(imageId) {
    fetch(`/image/${imageId}/delete/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.querySelector(`[data-image-id="${imageId}"]`).parentElement.remove();
        } else {
            alert('Ошибка при удалении изображения. Попробуйте еще раз.');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка. Попробуйте еще раз.');
    });
}
document.querySelectorAll('[data-image-id]').forEach(button => {
    button.addEventListener('click', function() {
        const imageId = this.getAttribute('data-image-id');
        if (confirm('Вы уверены, что хотите удалить это изображение?')) {
            deleteImage(imageId);
        }
    });
});

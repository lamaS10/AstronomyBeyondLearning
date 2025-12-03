document.addEventListener('DOMContentLoaded', () => {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookies[i].substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');


    async function toggleLike(postId, likeButton) {
        const url = `/post/${postId}/like/`;
        const icon = likeButton.querySelector('i'); 
        
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken, 
                    'Content-Type': 'application/json'
                },
            });

            if (!response.ok) {
                throw new Error(`Server responded with status: ${response.status}`);
            }

            const data = await response.json(); 
            const likeCountElement = likeButton.querySelector('.like-count');

            if (data.is_liked) {
                likeButton.classList.add('liked');
                icon.textContent = 'favorite'; 
            } else {
                likeButton.classList.remove('liked');
                icon.textContent = 'favorite_border'; 
            }
            
            if (likeCountElement) {
                likeCountElement.textContent = formatCount(data.total_likes);
            }

        } catch (error) {
            console.error('Error toggling like:', error);
            if (error.message.includes('403')) {
                 alert("Please log in to like this post.");
            } else {
                 alert("Could not process the request. Please try again later.");
            }
        }
    }

    function formatCount(num) {
        if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    }
    
    document.body.addEventListener('click', (e) => {
        const likeButton = e.target.closest('.like-btn'); 

        if (likeButton) {
            e.preventDefault(); 
            const postId = likeButton.dataset.postId; 
            
            if (postId) {
                toggleLike(postId, likeButton);
            }
        }
    });

    const deleteForm = document.getElementById('delete-post-form');

    if (deleteForm) {
        deleteForm.addEventListener('submit', function(e) {
            e.preventDefault(); 
            const confirmed = confirm("Are you sure you want to delete this post? This action cannot be undone.");
            
            if (confirmed) {
                const url = deleteForm.getAttribute('action');
                
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json'
                    },
                })
                .then(response => {
                    if (response.status === 200) {
                        return response.json();
                    } else if (response.status === 403) {
                        alert("Error: You do not have permission to delete this post.");
                        return Promise.reject('Forbidden');
                    } else {
                        alert("An error occurred while deleting the post.");
                        return Promise.reject('Error');
                    }
                })
                .then(data => {
                    if (data.success) {
                        alert(data.message);
                        window.location.href = "/"; 
                    }
                })
                .catch(error => {
                    console.error('Fetch error:', error);
                });
            }
        });
    }

    document.querySelectorAll('.delete-comment-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const commentId = this.dataset.commentId; 
            const deleteUrl = `/comment/${commentId}/delete/`;
            const commentElement = this.closest('.comment-item'); 

            const confirmed = confirm("Are you sure you want to delete this comment?");
            
            if (confirmed) {
                fetch(deleteUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json'
                    },
                })
                .then(response => {
                    if (response.status === 200) {
                        return response.json();
                    } else if (response.status === 403) {
                        alert("Error: You do not have permission to delete this comment.");
                        return Promise.reject('Forbidden');
                    } else {
                        alert("An error occurred while deleting the comment.");
                        return Promise.reject('Error');
                    }
                })
                .then(data => {
                    if (data.success) {
                        commentElement.remove();
                    }
                })
                .catch(error => {
                    console.error('Fetch error:', error);
                });
            }
        });
    });


    document.querySelectorAll('.bookmark-toggle').forEach(button => {
        const icon = button.querySelector('i'); 

        button.addEventListener('click', function(e) {
            e.preventDefault(); 
            const postId = this.dataset.postId;
            const url = `/post/${postId}/bookmark/`; 

            if (!icon) {
                console.error("Bookmark icon not found inside the button.");
                return;
            }

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                    alert("Please log in to save this post.");
                    return Promise.reject('Not authenticated');
                }
                return response.json();
            })
            .then(data => {
                if (data.is_bookmarked) {
                    icon.textContent = 'bookmark'; 
                    this.classList.add('bookmarked'); 
                    this.classList.remove('not-bookmarked');
                } else {
                    icon.textContent = 'bookmark_border'; 
                    this.classList.add('not-bookmarked');
                    this.classList.remove('bookmarked');
                }
                console.log(data.message);
            })
            .catch(error => {
                console.error('Bookmark error:', error);
            });
        });
    });

});

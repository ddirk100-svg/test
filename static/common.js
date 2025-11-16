// ========================================
// 공통 JavaScript 함수
// ========================================

/**
 * 공유 기능 (Web Share API 또는 클립보드)
 */
function shareArticle(url, title) {
    if (navigator.share) {
        navigator.share({
            title: title,
            url: url
        }).catch((error) => console.log('공유 취소'));
    } else {
        navigator.clipboard.writeText(url).then(() => {
            alert('링크가 클립보드에 복사되었습니다!\n\n' + url);
        }).catch(() => {
            prompt('이 링크를 복사하세요:', url);
        });
    }
}

/**
 * 페이지 로드 시 캐시 방지 (뒤로가기 대응)
 */
function preventCacheOnPageShow() {
    window.addEventListener('pageshow', function(event) {
        if (event.persisted || (window.performance && window.performance.navigation.type === 2)) {
            window.location.reload();
        }
    });
}


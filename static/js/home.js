$(document).ready(function () {
    bindEvents();
});


const bindEvents = _ => {
    $("#btn-access-user-area").on("click", _ => {
        accessUserArea()
    });
}

const accessUserArea = _ => {
    const usernameInput = $("#username-input");
    const username = usernameInput.val();

    if (!username) {
        usernameInput.addClass('is-invalid');
        return;
    }

    usernameInput.removeClass('is-invalid');
    getTransactions(username);
}


const showToast = (message, type) => {
    $("#toastMessage").text(message);
    $("#resultToast").removeClass("bg-primary bg-success bg-danger").addClass(`bg-${type}`);
    
    const toastElement = document.getElementById("resultToast");
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
};

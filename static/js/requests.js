const getTransactions = (username) => {
    $.ajax({
        url: `/users/${username}/transactions`,
        method: "GET",
        success: (response) => {
            console.log(response)
        },
        error: _ => {
            showToast("Algo deu errado ao acessar este usuário.", "danger")
        }
    });
}
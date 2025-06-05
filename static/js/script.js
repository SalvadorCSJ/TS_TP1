$(document).ready(function () {
    bindEvents();
});

const bindEvents = _ => {
    $('.btn-access-user-area').on('click', _ => {
        accessUserArea();
    });

    $('.username-input').on('keypress', (event) => {
        const ENTER_KEY_CODE = 13;
        if (event.which == ENTER_KEY_CODE) {
            $('.btn-access-user-area').click();
        }
    });

    $('.btn-show-add-modal').on('click', _ => {
        showAddModal();
    });

    $('.btn-add-transaction').on('click', _ => {
        if (validateAddInput()) {
            let transaction = getAddModalTransaction();
            addTransaction(transaction);
        }
    });

    $('.btn-show-update-modal').on('click', _ => {
        showUpdateModal();
    });

    $('.btn-update-transaction').on('click', _ => {
        if (validateEditInput()) {
            let transaction = getEditModalTransaction();
            updateTransaction(transaction);
        }
    });

    $('.btn-filter-all-transactions').on('click', _ => {
        clearFilters();
        $('.btn-filter-all-transactions').addClass('active');
        getAllTransactions();
    });

    $('.btn-filter-credits').on('click', _ => {
        clearFilters();
        $('.btn-filter-credits').addClass('active');
        getCredits();
    });

    $('.btn-filter-debits').on('click', _ => {
        clearFilters();
        $('.btn-filter-debits').addClass('active');
        getDebits();
    });

    $('.btn-filter-month').on('click', _ => {
        showMonthFilterModal();
    });

    $('.category-filter').on('change', _ => {
        const categoryFilter = $('.category-filter');
        const selectedCategory = categoryFilter.val();
        clearFilters();
        if (selectedCategory == 'Todas as categorias') {
            $('.btn-filter-all-transactions').click();
        }
        else {
            getTransactionsByCategory(selectedCategory);
        }
    });

    $('.btn-apply-month-filter').on('click', _ => {
        const yearInput = $('.filter-year-input');
        const monthInput = $('.filter-month-input');

        const month = monthInput.val();
        const year = yearInput.val();

        monthName = monthInput.find('option:selected').text();

        if (!year) {
            yearInput.addClass('is-invalid');
        }
        else {
            yearInput.removeClass('is-invalid');
            getTransactionsByMonth(year, month);
            clearFilters();
            $('.btn-filter-month').text(`${monthName} de ${year}`);
            $('.btn-filter-month').addClass('active');

        }
    });
}

const showMonthFilterModal = () => {
    const monthInput = $('.filter-month-input');
    const yearInput = $('.filter-year-input');
    const currentDate = new Date();

    yearInput.removeClass('is-invalid');
    yearInput.val(currentDate.getFullYear());
    monthInput.val(currentDate.getMonth() + 1);
    
    const modalElement = document.getElementById('monthFilterModal');
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
}

const clearFilters = _ => {
    $('btn-filter-month').removeClass('active')
    $('.btn-filter-all-transactions').removeClass('active');
    $('.btn-filter-credits').removeClass('active');
    $('.btn-filter-debits').removeClass('active');
    $('.btn-filter-month').removeClass('active');
    $('.btn-filter-month').text('Filtrar por mês');
}

const getAddModalTransaction = _ => {
    return {
        date: $('.new-transaction-date-input').val(),
        description: $('.new-transaction-description-input').val(),
        category: $('.new-transaction-category-input').val(),
        amount: $('.new-transaction-amount-input').val(),
        type: $('.new-transaction-type-input').val(),
    };
}

const validateAddInput = _ => {
    let isValid = true;
    const transaction = getAddModalTransaction();

    if (!transaction.date) {
        $('.new-transaction-date-input').addClass('is-invalid');
        isValid = false;
    }
    if (!transaction.description) {
        $('.new-transaction-description-input').addClass('is-invalid');
        isValid = false;
    }
    if (!transaction.category) {
        $('.new-transaction-category-input').addClass('is-invalid');
        isValid = false;
    }
    if (!transaction.amount) {
        $('.new-transaction-amount-input').addClass('is-invalid');
        isValid = false;
    }

    return isValid;
}

const validateEditInput = _ => {
    let isValid = true;
    const transaction = getEditModalTransaction();

    if (!transaction.date) {
        $('.update-transaction-date-input').addClass('is-invalid');
        isValid = false;
    }
    if (!transaction.description) {
        $('.update-transaction-description-input').addClass('is-invalid');
        isValid = false;
    }
    if (!transaction.category) {
        $('.update-transaction-category-input').addClass('is-invalid');
        isValid = false;
    }
    if (!transaction.amount) {
        $('.update-transaction-amount-input').addClass('is-invalid');
        isValid = false;
    }

    return isValid;
}

const getEditModalTransaction = _ => {
    return {        
        id: $('#updateTransactionModal').data('id'),
        date: $('.update-transaction-date-input').val(),
        description: $('.update-transaction-description-input').val(),
        category: $('.update-transaction-category-input').val(),
        amount: $('.update-transaction-amount-input').val(),
        type: $('.update-transaction-type-input').val(),
    };
}

const showAddModal = _ => {
    $('.new-transaction-date-input').val(formatDateToYYYYMMDD(new Date()));
    $('.new-transaction-description-input').val('');
    $('.new-transaction-category-input').val('');
    $('.new-transaction-amount-input').val('');
    $('.new-transaction-type-input').val('Receita');

    const modalElement = document.getElementById('addTransactionModal');
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
};

const formatDateToYYYYMMDD = (date) => {
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');

    return `${year}-${month}-${day}`;
}

function formatDate(yyyyMmDd) {
    const parts = yyyyMmDd.split('-');
    const year = parts[0];
    const month = parts[1];
    const day = parts[2];
    return `${day}/${month}/${year}`;
}

const accessUserArea = _ => {
    const usernameInput = $('.username-input');
    const username = usernameInput.val();

    if (!username) {
        usernameInput.addClass('is-invalid');
        return;
    }

    $('.subpage-home').remove();
    $('.subpage-transactions').show();
    $('.subpage-transactions').data('username', username);
    $('.subpage-transactions .username-display').text(username)
    $('.btn-filter-all-transactions').addClass('active');
    getAllTransactions();
}

const getAllTransactions = () => {
    const username = $('.subpage-transactions').data('username');
    $.ajax({
        url: `/users/${username}/transactions`,
        method: 'GET',
        success: (response) => {
            buildTransactionCards(response);
        },
        error: _ => {
            showToast('Ocorreu um erro ao tentar recuperar as transações.', 'danger')
        }
    });
}

const getCredits = () => {
    const username = $('.subpage-transactions').data('username');
    $.ajax({
        url: `/users/${username}/transactions/credits`,
        method: 'GET',
        success: (response) => {
            buildTransactionCards(response);
        },
        error: _ => {
            showToast('Ocorreu um erro ao tentar recuperar as transações.', 'danger')
        }
    });
}

const getDebits = () => {
    const username = $('.subpage-transactions').data('username');
    $.ajax({
        url: `/users/${username}/transactions/debits`,
        method: 'GET',
        success: (response) => {
            buildTransactionCards(response);
        },
        error: _ => {
            showToast('Ocorreu um erro ao tentar recuperar as transações.', 'danger')
        }
    });
}

const getTransactionsByCategory = (category) => {
    const username = $('.subpage-transactions').data('username');
    $.ajax({
        url: `/users/${username}/transactions/category/${category}`,
        method: 'GET',
        success: (response) => {
            buildTransactionCards(response);
            setCategoriesFilter(category);
        },
        error: _ => {
            showToast('Ocorreu um erro ao tentar recuperar as transações.', 'danger')
        }
    });
}

const getTransactionsByMonth = (year, month) => {
    const username = $('.subpage-transactions').data('username');
    $.ajax({
        url: `/users/${username}/transactions/month/${year}/${month}`,
        method: 'GET',
        success: (response) => {
            const modalElement = document.getElementById('monthFilterModal');
            const modal = bootstrap.Modal.getInstance(modalElement);
            modal.hide();
            buildTransactionCards(response);
        },
        error: _ => {
            showToast('Ocorreu um erro ao tentar recuperar as transações.', 'danger')
        }
    });
}

const buildTransactionCards = (transactions) => {
    const transactionsPlaceholder = $('.transactions-placeholder');
    const transactionsContainer = $('.transactions-container');
    transactionsContainer.empty();

    if (transactions.length == 0) {
        transactionsPlaceholder.css('display', 'flex');
    }

    transactions = transactions.sort((a, b) => b.date.localeCompare(a.date))

    for (const transaction of transactions) {
        buildTransactionCard(transaction);
    }

    setCategoriesFilter();
}

const buildTransactionCard = (transaction) => {
    $('.transactions-placeholder').hide();

    const transactionsContainer = $('.transactions-container');
    const transactionCard = $(`
        <div class="transaction-card card" data-id=${transaction.id}>
            <div class="card-body d-flex align-items-start gap-2">
                <div class="flex-grow-1">
                    <div class="transaction-card-date">${formatDate(transaction.date)}</div>
                    <div class="transaction-card-category">${transaction.category}</div>
                    <div class="transaction-card-amount">R$ <span class="amount-value">${transaction.amount}</span></div>
                    <div class="transaction-card-description text-secondary">${transaction.description}</div>
                </div>
                <button type="button" class="btn btn-light btn-update-transaction" title="Editar transação">
                    <i class="bi bi-pencil"></i>
                </button>
                <button type="button" class="btn btn-light btn-delete-transaction" title="Excluir transação">
                    <i class="bi bi-x-lg"></i>
                </button>
            </div>
        </div>
    `).appendTo(transactionsContainer);
    
    const transactionCardAmount =  transactionCard.find('.transaction-card-amount');

    if (transaction.type == "Despesa") {
        transactionCardAmount.removeClass('text-success');
        transactionCardAmount.addClass('text-danger');
    }
    else {
        transactionCardAmount.removeClass('text-danger');
        transactionCardAmount.addClass('text-success');
    }

    transactionCard.data('transaction', transaction);
    transactionCard.data('id', transaction.id);
    bindTransactionCardEvents(transactionCard)

    updateSum();

    return transactionCard;
}

const bindTransactionCardEvents = (selector) => {
    $(selector).find(".btn-update-transaction").on("click", event => {
        const transactionCard = $(event.currentTarget).closest(".transaction-card");
        const transaction = transactionCard.data("transaction");
        showEditModal(transaction);
    });
    
    $(selector).find(".btn-delete-transaction").on("click", event => {
        const transactionCard = $(event.currentTarget).closest(".transaction-card");
        const transaction = transactionCard.data("transaction");
        const id = transaction.id;
        deleteTransaction(id);
    });
}

const showEditModal = (transaction) => {
    $("#updateTransactionModal").data("id", transaction.id);
    $('.update-transaction-date-input').val(transaction.date);
    $('.update-transaction-description-input').val(transaction.description);
    $('.update-transaction-category-input').val(transaction.category);
    $('.update-transaction-amount-input').val(transaction.amount);
    $('.update-transaction-type-input').val(transaction.type);

    const modalElement = document.getElementById("updateTransactionModal");
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
}

const addTransaction = (transaction) => {
    const username = $('.subpage-transactions').data('username');
    $.ajax({
        url: `/users/${username}/transactions`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            date: transaction.date,
            description: transaction.description,
            category: transaction.category,
            amount: transaction.amount,
            type: transaction.type,
        }),
        success: (response) => {
            const modalElement = document.getElementById('addTransactionModal');
            const modal = bootstrap.Modal.getInstance(modalElement);
            modal.hide();

            showToast(response.message, 'success');
            transaction.id = response.transactionId;
            buildTransactionCard(transaction);
            updateTransactionsList();
        },
        error: _ => {
            showToast('Algo deu errado ao criar a transação.', 'danger')
        }
    });
}

const updateTransaction = (transaction) => {
    const username = $('.subpage-transactions').data('username');
    $.ajax({
        url: `/users/${username}/transactions/${transaction.id}`,
        method: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify({
            id: transaction.id,
            date: transaction.date,
            description: transaction.description,
            category: transaction.category,
            amount: transaction.amount,
            type: transaction.type,
        }),
        success: (response) => {
            const modalElement = document.getElementById('updateTransactionModal');
            const modal = bootstrap.Modal.getInstance(modalElement)
            modal.hide();

            showToast(response.message, 'success');

            const transactionCard = $(`.transaction-card[data-id=${transaction.id}]`);
            transactionCard.data('transaction', transaction);
            transactionCard.find('.transaction-card-date').text(formatDate(transaction.date));
            transactionCard.find('.transaction-card-category').text(transaction.category);
            transactionCard.find('.transaction-card-amount .amount-value').text(transaction.amount);
            transactionCard.find('.transaction-card-description').text(transaction.description);
            
            updateTransactionsList();
        },
        error: _ => {
            showToast('Algo deu errado ao atualizar a transação.', 'danger')
        }
    });
}

const deleteTransaction = (id) => {
    const username = $('.subpage-transactions').data('username');
    $.ajax({
        url: `/users/${username}/transactions/${id}`,
        method: 'DELETE',
        success: (response) => {
            showToast(response.message, 'success');

            const transactionCard = $(`.transaction-card[data-id=${id}]`);
            transactionCard.remove();

            if ($('.transaction-card').length == 0) {
                $('.transactions-placeholder').show();
            }

            updateTransactionsList();
        },
        error: _ => {
            showToast('Algo deu errado ao excluir a transação.', 'danger')
        }
    });
}

const updateSum = () => {
    let sum = 0;
    $('.transaction-card').each((_, element) => {
        const transaction = $(element).data('transaction');
        sum += (transaction.type == "Despesa") ? (-transaction.amount) : (transaction.amount);
    });
    const transactionsSum = $('.transactions-sum');
    transactionsSum.text(sum.toFixed(2));
    
    if (sum < 0) {
        transactionsSum.removeClass('text-success');
        transactionsSum.addClass('text-danger');
    }
    else {
        transactionsSum.removeClass('text-danger');
        transactionsSum.addClass('text-success');
    }
}

const updateTransactionsList = () => {
    let transactions = [];
    $('.transaction-card').each((_, element) => {
        transactions.push($(element).data('transaction'));
    });

    buildTransactionCards(transactions);
}

const setCategoriesFilter = (selectedCategory) => {
    let categories = [];
    $('.transaction-card').each((_, element) => {
        categories.push($(element).data('transaction').category);
    });
    categories = [...new Set(categories)];

    categoriesSelect = $('.category-filter');
    categoriesSelect.empty();

    categoriesSelect.append($('<option>', {
        text : 'Todas as categorias'
    }));

    for (const category of categories) {
        categoriesSelect.append($('<option>', {
            value: category,
            text : category,
            selected: category == selectedCategory
        }));
    }
}


const showToast = (message, type) => {
    $('.toastMessage').text(message);
    $('#resultToast').removeClass('bg-primary bg-success bg-danger').addClass(`bg-${type}`);
    
    const toastElement = document.getElementById('resultToast');
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
};
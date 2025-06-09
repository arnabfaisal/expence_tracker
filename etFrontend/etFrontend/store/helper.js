// export function handler(initialTotal, transactions) {
//     const totalData = {
//         created_at: [],
//         amount: []
//     };
//     const incomeData = {
//         created_at: [],
//         amount: []
//     };
//     const expenseData = {
//         created_at: [],
//         amount: []
//     };

//     let runningTotal = initialTotal; // Track running balance

//     transactions.forEach(transaction => {
//         const amount = parseFloat(transaction.amount);
//         const date = transaction.created_at.slice(0,19); // Consistent date format

//         if (transaction.transaction_type === 'income') {
//             incomeData.created_at.push(date);
//             incomeData.amount.push(amount);
//             runningTotal += amount;
//         } else if (transaction.transaction_type === 'expense') {
//             expenseData.created_at.push(date);
//             expenseData.amount.push(amount);
//             runningTotal -= amount;
//         }

//         totalData.created_at.push(date);
//         totalData.amount.push(runningTotal);
//     });

//     return { totalData, incomeData, expenseData };
// }
export function handler(initialTotal, transactions) {
  const totalData = [];
  const incomeData = [];
  const expenseData = [];

  let runningTotal = initialTotal;

  const sortedTransactions = [...transactions].sort(
    (a, b) => new Date(a.created_at) - new Date(b.created_at)
  );

  sortedTransactions.forEach((transaction) => {
    const amount = parseFloat(transaction.amount);
    const date = transaction.created_at.slice(0, 19); // e.g., "2025-06-09T20:17:11"

    if (transaction.transaction_type === 'income') {
      incomeData.push({ x: date, y: amount });
      runningTotal += amount;
    } else if (transaction.transaction_type === 'expense') {
      expenseData.push({ x: date, y: amount });
      runningTotal -= amount;
    }

    totalData.push({ x: date, y: runningTotal });
  });

  return { totalData, incomeData, expenseData };
}

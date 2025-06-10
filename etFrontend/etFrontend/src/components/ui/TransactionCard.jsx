import React from "react";

function TransactionCard({transaction}) {
  return (
    <div className="">
      <div className="h-[200px] w-[300px] md:w-[300px] bg-white shadow-2xl shadow-[#A5B4FC] rounded-2xl">
        <div className="flex justify-between gap-2 px-3 py-2">
          <div>
          <h1 className="md:text-3xl font-myfamily myfontdesign">{transaction.amount}$</h1>
          </div>
          <div className={`px-4 rounded-xl flex items-center justify-center ${transaction.transaction_type ==='income' ? 'bg-shobuj': 'bg-laal'}`}>
            <p className="font-myfamily">{transaction.transaction_type}</p>
          </div>
        </div>
        <div className="mt-4 px-3">
          <h1>{transaction.category.name}</h1>
        </div>
        <div className="mt-4 px-3">
          <h1>{transaction.description}</h1>
        </div>
        <div className="mt-4 px-3">
          <p>{transaction.date.slice(0,10)}</p>
        </div>
      </div>
    </div>
  );
}

export default TransactionCard;

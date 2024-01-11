export const curReal = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' })
export const fmtReal = (value) => curReal.format(value)


// let USDollar = new Intl.NumberFormat('en-US', {
//     style: 'currency',
//     currency: 'USD',
// });

import type {
    OnReadyCallback,
    DatafeedConfiguration,
    ResolutionString,
    SearchSymbolsCallback,
    ResolveCallback,
    SymbolResolveExtension,
    SearchSymbolResultItem,
    LibrarySymbolInfo,
} from "charting_library";

const configurationData: DatafeedConfiguration = {
    supported_resolutions: ["1D", "1W", "1M"] as ResolutionString[],
    exchanges: [
        {
            value: "Bitfinex",
            name: "Bitfinex",
            desc: "Bitfinex",
        },
        {
            // `exchange` argument for the `searchSymbols` method, if a user selects this exchange
            value: "Kraken",
            // filter name
            name: "Kraken",
            // full exchange name displayed in the filter popup
            desc: "Kraken bitcoin exchange",
        },
    ],
    symbols_types: [
        {
            name: "crypto",
            // `symbolType` argument for the `searchSymbols` method, if a user selects this symbol type
            value: "crypto",
        },
        // ...
    ],
};

export const allSymbols: SearchSymbolResultItem[] = [];

export const onReady = (callback: OnReadyCallback): void => {
    console.log("[onReady]: Method call");
    setTimeout(() => callback(configurationData));
};

export const searchSymbols = (
    userInput: string,
    exchange: string,
    symbolType: string,
    onResult: SearchSymbolsCallback
): void => {
    console.log("[searchSymbols]: Method call");
    const symbols = allSymbols;

    onResult(
        symbols.filter((symbol) => {
            const isExchangeValid =
                exchange === "" || symbol.exchange === exchange;
            const isFullSymbolContainsInput =
                symbol.full_name
                    .toLowerCase()
                    .indexOf(userInput.toLowerCase()) !== -1;
            return isExchangeValid && isFullSymbolContainsInput;
        })
    );
};

export const resolveSymbol = (
    symbolName: string,
    onResolve: ResolveCallback,
    onError: ErrorCallback,
    extension?: SymbolResolveExtension
): void => {
    console.log("[resolveSymbol]: Method call", symbolName);
    const symbols = allSymbols;
    const symbolItem = symbols.find(
        (symbol) => symbol.full_name === symbolName
    );
    if (symbolItem === undefined) {
        console.log("[resolveSymbol]: Cannot resolve symbol", symbolName);
        onError(new DOMException("cannot resolve symbol"));
        return;
    }
    const symbolInfo: LibrarySymbolInfo = {
        ticker: symbolItem.full_name,
        name: symbolItem.symbol,
        description: symbolItem.description,
        type: symbolItem.type,
        session: "24x7",
        timezone: "Etc/UTC",
        exchange: symbolItem.exchange,
        minmov: 1,
        pricescale: 100,
        has_intraday: false,
        has_no_volume: true,
        has_weekly_and_monthly: false,
        supported_resolutions:
            configurationData.supported_resolutions ??
            (["D"] as ResolutionString[]),
        volume_precision: 2,
        data_status: "streaming",
        full_name: "",
        listed_exchange: "",
        format: "price",
    };
    console.log("[resolveSymbol]: Symbol resolved", symbolName);
    onResolve(symbolInfo);
};

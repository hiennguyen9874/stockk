import type {
  OnReadyCallback,
  DatafeedConfiguration,
  ResolutionString,
  SearchSymbolsCallback,
  ResolveCallback,
  SymbolResolveExtension,
  SearchSymbolResultItem,
  LibrarySymbolInfo,
  PeriodParams,
  HistoryCallback,
  Bar,
  SubscribeBarsCallback,
  ErrorCallback,
} from 'charting_library';
import * as tcbsService from 'api/tcbs';

export const exchangeToValue: {
  [key: string]: string;
} = {
  '0': 'HOSE',
  '2': 'HNX',
  '3': 'UPCOM',
};

const configurationData: DatafeedConfiguration = {
  supported_resolutions: ['1D', '1W', '1M'] as ResolutionString[],
  exchanges: [
    {
      // `exchange` argument for the `searchSymbols` method, if a user selects this exchange
      value: 'HOSE',
      // filter name
      name: 'HOSE',
      // full exchange name displayed in the filter popup
      desc: 'HOSE',
    },
    {
      // `exchange` argument for the `searchSymbols` method, if a user selects this exchange
      value: 'HNX',
      // filter name
      name: 'HNX',
      // full exchange name displayed in the filter popup
      desc: 'HNX',
    },
    {
      // `exchange` argument for the `searchSymbols` method, if a user selects this exchange
      value: 'UPCOM',
      // filter name
      name: 'UPCOM',
      // full exchange name displayed in the filter popup
      desc: 'UPCOM',
    },
  ],
  symbols_types: [
    {
      name: 'stock',
      value: 'stock',
    },
    {
      name: 'crypto',
      value: 'crypto',
    },
  ],
};

export const allSymbols: SearchSymbolResultItem[] = [];

export const onReady = (callback: OnReadyCallback): void => {
  console.log('[onReady]: Method call');
  setTimeout(() => callback(configurationData));
};

export const searchSymbols = (
  userInput: string,
  exchange: string,
  symbolType: string,
  onResult: SearchSymbolsCallback
): void => {
  console.log('[searchSymbols]: Method call');

  tcbsService
    .searchSymbolsByKey(userInput)
    .then(({ data }) => {
      onResult(
        data
          .filter((symbol) => {
            const isExchangeValid =
              exchange === '' ||
              (Object.keys(exchangeToValue).includes(symbol.exchange) &&
                exchangeToValue[symbol.exchange]);
            const isFullSymbolContainsInput =
              symbol.value.toLowerCase().indexOf(userInput.toLowerCase()) !==
              -1;
            return isExchangeValid && isFullSymbolContainsInput;
          })
          .map((symbol) => ({
            symbol: symbol.name,
            full_name: symbol.value,
            description: symbol.value,
            exchange: 'HOSE',
            ticker: symbol.name,
            type: symbol.type,
          }))
      );
    })
    .catch(() => {});
};

export const resolveSymbol = (
  symbolName: string,
  onResolve: ResolveCallback,
  onError: ErrorCallback,
  extension?: SymbolResolveExtension
): void => {
  console.log('[resolveSymbol]: Method call', symbolName);
  const symbols = allSymbols;
  const symbolItem = symbols.find((symbol) => symbol.full_name === symbolName);
  if (symbolItem === undefined) {
    console.log('[resolveSymbol]: Cannot resolve symbol', symbolName);
    onError('cannot resolve symbol');
    return;
  }
  const symbolInfo: LibrarySymbolInfo = {
    ticker: symbolItem.full_name,
    name: symbolItem.symbol,
    description: symbolItem.description,
    type: symbolItem.type,
    session: '24x7',
    timezone: 'Etc/UTC',
    exchange: symbolItem.exchange,
    minmov: 1,
    pricescale: 100,
    has_intraday: false,
    has_no_volume: true,
    has_weekly_and_monthly: false,
    supported_resolutions:
      configurationData.supported_resolutions ?? (['D'] as ResolutionString[]),
    volume_precision: 2,
    data_status: 'streaming',
    full_name: '',
    listed_exchange: '',
    format: 'price',
  };
  console.log('[resolveSymbol]: Symbol resolved', symbolName);
  onResolve(symbolInfo);
};

export const getBars = (
  symbolInfo: LibrarySymbolInfo,
  resolution: ResolutionString,
  periodParams: PeriodParams,
  onResult: HistoryCallback,
  onError: ErrorCallback
): void => {
  const { from, to, firstDataRequest } = periodParams;
  console.log('[getBars]: Method call', symbolInfo, resolution, from, to);

  const bars: Bar[] = [];
  onResult(bars, { noData: false });
};

export const subscribeBars = (
  symbolInfo: LibrarySymbolInfo,
  resolution: ResolutionString,
  onTick: SubscribeBarsCallback,
  listenerGuid: string,
  onResetCacheNeededCallback: () => void
): void => {
  console.log('[subscribeBars]: Method call with subscriberUID:', listenerGuid);
};

export const unsubscribeBars = (listenerGuid: string): void => {
  console.log(
    '[unsubscribeBars]: Method call with listenerGuid:',
    listenerGuid
  );
};

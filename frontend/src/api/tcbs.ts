/* eslint-disable camelcase */
import { AxiosResponse } from 'axios';

import authHeader, { axiosInstance } from './auth-header';

const API_URL = '/api/v0/tcbs/';

export interface SearchSymbolResultItem {
  name: string;
  value: string;
  type: string;
  exchange: string;
  industry: string | null;
}

export const searchSymbolsByKey = (
  key: string
): Promise<AxiosResponse<SearchSymbolResultItem[]>> =>
  axiosInstance.get(`${API_URL}search`, {
    headers: authHeader(),
    params: {
      key,
    },
  });

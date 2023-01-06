/**
 * See:
 *  <https://en.wikipedia.org/wiki/Box_plot#cite_note-frigge_hoaglin_iglewicz-2>
 *  <http://stat.ethz.ch/R-manual/R-devel/library/grDevices/html/boxplot.stats.html>
 *
 * Helper method for preparing data.
 *
 * @param {Array.<number>} rawData like
 *        [
 *            [12,232,443], (raw data set for the first box)
 *            [3843,5545,1232], (raw data set for the second box)
 *            ...
 *        ]
 * @param {Object} [opt]
 *
 * @param {(number|string)} [opt.boundIQR=1.5] Data less than min bound is outlier.
 *      default 1.5, means Q1 - 1.5 * (Q3 - Q1).
 *      If 'none'/0 passed, min bound will not be used.
 * @param {(number|string)} [opt.layout='horizontal']
 *      Box plot layout, can be 'horizontal' or 'vertical'
 * @return {Object} {
 *      boxData: Array.<Array.<number>>
 *      outliers: Array.<Array.<number>>
 *      axisData: Array.<string>
 * }
 */
export default function (rawData: number[][], opt: {
    boundIQR?: number | 'none';
    layout?: 'horizontal' | 'vertical';
}): {
    boxData: number[][];
    outliers: number[][];
    axisData: string[];
};

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS-IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * @fileoverview Factory for handling warnings.
 *
 * @author sll@google.com (Sean Lip)
 */

oppia.factory('warningsData', function($rootScope) {
  var warningsData = {warnings: []};
  var MAX_WARNINGS = 5;

  /**
   * Adds a warning message to the butterbar.
   * @param {string} warning The warning message to display.
   */
  warningsData.addWarning = function(warning) {
    console.log('WARNING: ' + warning);
    if (warningsData.warnings.length < MAX_WARNINGS) {
      warningsData.warnings.push(warning);
    }
  };

  /**
   * Deletes the warning at a given index.
   * @param {int} index The index of the warning to delete.
   */
  warningsData.deleteWarning = function(index) {
    warningsData.warnings.splice(index, 1);
  };

  /**
   * Clears all warnings.
   */
  warningsData.clear = function() {
    warningsData.warnings = [];
  };

  return warningsData;
});
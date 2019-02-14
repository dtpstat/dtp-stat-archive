<template>
  <div class="extra-stats-section collapse flex-grow-1" data-parent=".map-with-stats">
    <table class="extra-stats table table-borderless">
      <thead>
        <tr>
          <th class="mvc-types-col">По видам</th>
          <th>По нарушениям</th>
        </tr>
      </thead>

      <tbody>
        <tr>
          <td>
            <table class="table stats-counts-list list-unstyled">
              <tbody>{this.props.countsByMvcTypes.map(row => (
                <tr key="{row.id}">
                  <td class="var_name">{mvcTypes[row.id].name}</td>
                  <td class="value">{row.count}</td>
                </tr>))}
              </tbody>
            </table>
          </td>

          <td>
            <table class="table stats-counts-list list-unstyled">
              <tbody>{this.props.countsByOffences.map(row => (
                <tr key="{row.id}">
                  <td class="var_name">{offences[row.id].name}</td>
                  <td class="value">{row.count}</td>
                </tr>))}
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "dtp-extra-stats"
};
</script>

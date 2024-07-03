<template>
  <div>
    <v-layout wrap>
      <v-flex xs12 sm12 md4 mt-3 pl-4>
        <v-toolbar-title>{{ $t('business.TITLE') }}</v-toolbar-title>
      </v-flex>
      <v-flex xs12 sm6 md4 px-3>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          :label="$t('dataTable.SEARCH')"
          single-line
          hide-details
          clearable
          clear-icon="mdi-close"
        ></v-text-field>
      </v-flex>
      <v-flex xs12 sm6 md4 text-xs-right mb-2 mt-2 pr-2>
        <v-dialog
          v-model="dialog"
          max-width="800px"
          content-class="dlgNewEditItem"
        >
          <template v-slot:activator="{ on }">
            <v-btn color="secondary" v-on="on" class="btnNewItem pr-4">
              <v-icon class="mr-2">mdi-plus</v-icon>
              {{ $t('dataTable.NEW_ITEM') }}
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>
            <v-card-text>
              <v-container grid-list-md>
                <v-layout wrap>
                  <template v-if="editedItem._id">
                    <v-flex xs12 md4>
                      <label for="createdAt">{{ $t('common.CREATED') }}</label>
                      <div name="createdAt">
                        {{ getFormat(editedItem.createdAt) }}
                      </div>
                    </v-flex>
                    <v-flex xs12 md4>
                      <label for="updatedAt">{{ $t('common.UPDATED') }}</label>
                      <div name="updatedAt">
                        {{ getFormat(editedItem.updatedAt) }}
                      </div>
                    </v-flex>
                  </template>
                  <v-flex xs12 md6>
                    <v-text-field
                      id="name"
                      name="name"
                      v-model="editedItem.name"
                      :label="$t('business.headers.NAME')"
                      :data-vv-as="$t('business.headers.NAME')"
                      :error-messages="errorMessages"
                      v-validate.disable="'required'"
                      autocomplete="off"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs12 md6>
                    <v-text-field
                      id="email"
                      name="email"
                      type="email"
                      v-model="editedItem.email"
                      :label="$t('business.headers.EMAIL')"
                      :data-vv-as="$t('business.headers.EMAIL')"
                      :error-messages="errorMessages"
                      v-validate.disable="'required|email'"
                      autocomplete="off"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs12 md6>
                    <v-text-field
                      id="businessType"
                      name="businessType"
                      v-model="editedItem.businessType"
                      :label="$t('business.headers.TYPE')"
                      :data-vv-as="$t('business.headers.TYPE')"
                      :error-messages="errorMessages"
                      autocomplete="off"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs12 md6>
                    <v-text-field
                      id="uri"
                      name="uri"
                      v-model="editedItem.uri"
                      :label="$t('business.headers.URI')"
                      :data-vv-as="$t('business.headers.URI')"
                      :error-messages="errorMessages"
                      autocomplete="off"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs12 md6>
                    <v-text-field
                      id="streetAddress"
                      name="streetAddress"
                      v-model="editedItem.streetAddress"
                      :label="$t('business.headers.STREET_ADDRESS')"
                      :data-vv-as="$t('business.headers.STREET_ADDRESS')"
                      :error-messages="errorMessages"
                      autocomplete="off"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs12 md6>
                    <v-autocomplete
                      id="addressLocality"
                      name="addressLocality"
                      :label="$t('business.headers.ADDRESS_LOCALITY')"
                      :search-input.sync="searchInput"
                      v-model="editedItem.addressLocality"
                      :items="allCities"
                      clearable
                      :data-vv-as="$t('business.headers.ADDRESS_LOCALITY')"
                      :error-messages="errorMessages"
                      v-validate.disable="'required'"
                      autocomplete="off"
                      class="inputCity"
                    />
                  </v-flex>
                  <v-flex xs12 md6>
                    <v-text-field
                      id="addressRegion"
                      name="addressRegion"
                      v-model="editedItem.addressRegion"
                      :label="$t('business.headers.ADDRESS_REGION')"
                      :data-vv-as="$t('business.headers.ADDRESS_REGION')"
                      :error-messages="errorMessages"
                      v-validate.disable="'required'"
                      autocomplete="off"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs12 md6>
                    <v-text-field
                      id="postalCode"
                      name="postalCode"
                      v-model="editedItem.postalCode"
                      :label="$t('business.headers.POSTAL_CODE')"
                      :data-vv-as="$t('business.headers.POSTAL_CODE')"
                      :error-messages="errorMessages"
                      autocomplete="off"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs12 md6>
                    <v-text-field
                      id="phone"
                      name="phone"
                      type="tel"
                      v-model="editedItem.phone"
                      :label="$t('business.headers.TELEPHONE')"
                      :data-vv-as="$t('business.headers.TELEPHONE')"
                      :error-messages="errorMessages"
                      autocomplete="off"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs12 md6>
                    <v-text-field
                      id="contact"
                      name="contact"
                      v-model="editedItem.contact"
                      :label="$t('business.headers.CONTACT_NAME')"
                      :data-vv-as="$t('business.headers.CONTACT_NAME')"
                      :error-messages="errorMessages"
                      autocomplete="off"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs12 md6>
                    <v-text-field
                      id="jobTitle"
                      name="jobTitle"
                      v-model="editedItem.jobTitle"
                      :label="$t('business.headers.JOB_TITLE')"
                      :data-vv-as="$t('business.headers.JOB_TITLE')"
                      :error-messages="errorMessages"
                      autocomplete="off"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs12 md6>
                    <v-text-field
                      id="contactPhone"
                      name="contactPhone"
                      type="tel"
                      v-model="editedItem.contactPhone"
                      :label="$t('business.headers.CONTACT_PHONE')"
                      :data-vv-as="$t('business.headers.CONTACT_PHONE')"
                      :error-messages="errorMessages"
                      autocomplete="off"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs12 md6>
                    <v-text-field
                      id="contactEmail"
                      name="contactEmail"
                      type="email"
                      v-model="editedItem.contactEmail"
                      :label="$t('business.headers.CONTACT_EMAIL')"
                      :data-vv-as="$t('business.headers.CONTACT_EMAIL')"
                      :error-messages="errorMessages"
                      autocomplete="off"
                    ></v-text-field>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="red lighten3"
                text
                @click="close"
                class="btnCancel"
                >{{ $t('dataTable.CANCEL') }}</v-btn
              >
              <v-btn
                color="yellow lighten3"
                text
                @click="save"
                class="btnSave"
                >{{ $t('dataTable.SAVE') }}</v-btn
              >
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-flex>
    </v-layout>
    <v-data-table
      :headers="headers"
      :items="items"
      :page.sync="page"
      :items-per-page="itemsPerPage"
      hide-default-footer
      :sort-by.sync="sortBy"
      :sort-desc.sync="sortDesc"
      item-key=""
      :search="search"
      :server-items-length="totalItems"
      class="elevation-1"
      @page-count="pageCount = $event"
      @pagination="doSomething"
    >
      <template v-slot:item._id="props">
        <v-layout class="justify-center">
          <v-tooltip top>
            <template #activator="on">
              <v-btn v-on="on" @click="editItem(props.item)" icon class="mx-0">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
            </template>
            <span>{{ $t('dataTable.EDIT') }}</span>
          </v-tooltip>
          <v-tooltip top>
            <template #activator="on">
              <v-btn
                icon
                color="yellow darken-1"
                class="mx-0"
                v-on="on"
                @click="deleteItem($event, props.item)"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
            <span>{{ $t('dataTable.DELETE') }}</span>
          </v-tooltip>
        </v-layout>
      </template>
      <template v-slot:no-data>{{ $t('dataTable.NO_DATA') }}</template>
      <template v-slot:no-results>{{ $t('dataTable.NO_RESULTS') }}</template>
    </v-data-table>
    <ErrorMessage />
    <SuccessMessage />
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import { getFormat, buildPayloadPagination } from '@/utils/utils.js'

export default {
  metaInfo() {
    return {
      title: this.$store.getters.appTitle,
      titleTemplate: `${this.$t('business.TITLE')} - %s`
    }
  },
  data() {
    return {
      searchInput: '',
      dataTableLoading: true,
      delayTimer: null,
      dialog: false,
      search: '',
      pagination: {},
      editedItem: {},
      defaultItem: {},
      fieldsToSearch: ['name', 'email', 'city', 'contact', 'phone'],
      page: 1,
      pageCount: 0,
      itemsPerPage: 10,
      sortBy: 'username',
      sortDesc: false,
      errorMessages: []
    }
  },
  computed: {
    roles() {
      return [
        { name: this.$t('roles.ADMIN'), value: 'admin' },
        { name: this.$t('roles.USER'), value: 'user' }
      ]
    },
    allCities() {
      return this.$store.state.cities.allCities
    },
    formTitle() {
      return this.editedItem._id
        ? this.$t('dataTable.EDIT_ITEM')
        : this.$t('dataTable.NEW_ITEM')
    },
    headers() {
      return [
        {
          text: this.$i18n.t('dataTable.ACTIONS'),
          value: '_id',
          sortable: false,
          width: 100
        },
        {
          text: this.$i18n.t('business.headers.NAME'),
          align: 'left',
          sortable: true,
          value: 'name'
        },
        {
          text: this.$i18n.t('business.headers.TELEPHONE'),
          align: 'left',
          sortable: true,
          value: 'phone'
        },
        {
          text: this.$i18n.t('business.headers.EMAIL'),
          align: 'left',
          sortable: true,
          value: 'email'
        },
        // {
        //   text: this.$i18n.t('business.headers.URI'),
        //   align: 'left',
        //   sortable: true,
        //   value: 'uri'
        // },
        {
          text: this.$i18n.t('business.headers.POSTAL_CODE'),
          align: 'left',
          sortable: true,
          value: 'postalCode'
        },
        // {
        //   text: this.$i18n.t('business.headers.TYPE'),
        //   align: 'left',
        //   sortable: true,
        //   value: 'businessType'
        // },
        // {
        //   text: this.$i18n.t('business.headers.STREET_ADDRESS'),
        //   align: 'left',
        //   sortable: true,
        //   value: 'streetAddress'
        // },
        {
          text: this.$i18n.t('business.headers.ADDRESS_LOCALITY'),
          align: 'left',
          sortable: true,
          value: 'addressLocality'
        },
        // {
        //   text: this.$i18n.t('business.headers.ADDRESS_REGION'),
        //   align: 'left',
        //   sortable: true,
        //   value: 'addressRegion'
        // },
        {
          text: this.$i18n.t('business.headers.CONTACT_NAME'),
          align: 'left',
          sortable: true,
          value: 'contact'
        },
        {
          text: this.$i18n.t('business.headers.JOB_TITLE'),
          align: 'left',
          sortable: true,
          value: 'jobTitle'
        },
        {
          text: this.$i18n.t('business.headers.CONTACT_PHONE'),
          align: 'left',
          sortable: true,
          value: 'contactPhone'
        },
        {
          text: this.$i18n.t('business.headers.CONTACT_EMAIL'),
          align: 'left',
          sortable: true,
          value: 'contactEmail'
        },
        {
          text: this.$i18n.t('common.CREATED'),
          align: 'left',
          sortable: true,
          value: 'createdAt'
        },
        {
          text: this.$i18n.t('common.UPDATED'),
          align: 'left',
          sortable: true,
          value: 'updatedAt'
        }
      ]
    },
    items() {
      return this.$store.state.adminBusinesses.businesses
    },
    totalItems() {
      return this.$store.state.adminBusinesses.totalBusinesses
    }
  },
  watch: {
    dialog(value) {
      return value ? true : this.close()
    },
    pagination: {
      async handler() {
        try {
          this.dataTableLoading = true
          await this.getBusinesses(
            buildPayloadPagination(this.pagination, this.buildSearch())
          )
          this.dataTableLoading = false
          // eslint-disable-next-line no-unused-vars
        } catch (error) {
          this.dataTableLoading = false
        }
      },
      deep: true
    },
    search() {
      clearTimeout(this.delayTimer)
      this.delayTimer = setTimeout(() => {
        this.doSearch()
      }, 400)
    }
  },
  methods: {
    ...mapActions([
      'getBusinesses',
      'getAllCities',
      'editBusiness',
      'saveBusiness',
      'deleteBusiness'
    ]),
    doSomething(v) {
      // console.log('pagination', v)
      this.pagination = v
    },
    getFormat(date) {
      window.__localeId__ = this.$store.getters.locale
      return getFormat(date, 'iii, MMMM d yyyy, h:mm a')
    },
    roleName(value) {
      return value === 'admin' ? this.$t('roles.ADMIN') : this.$t('roles.USER')
    },
    trueFalse(value) {
      return value
        ? '<i aria-hidden="true" class="v-icon mdi mdi-check green--text" style="font-size: 16px;"></i>'
        : '<i aria-hidden="true" class="v-icon mdi mdi-close red--text" style="font-size: 16px;"></i>'
    },
    async doSearch() {
      try {
        this.dataTableLoading = true
        await this.getBusinesses(
          buildPayloadPagination(this.pagination, this.buildSearch())
        )
        this.dataTableLoading = false
        // eslint-disable-next-line no-unused-vars
      } catch (error) {
        this.dataTableLoading = false
      }
    },
    buildSearch() {
      return this.search
        ? { query: this.search, fields: this.fieldsToSearch.join(',') }
        : {}
    },
    editItem(item) {
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },
    async deleteItem(item) {
      try {
        const response = await this.$confirm(
          this.$t('common.DO_YOU_REALLY_WANT_TO_DELETE_THIS_ITEM'),
          {
            title: this.$t('common.WARNING'),
            buttonTrueText: this.$t('common.DELETE'),
            buttonFalseText: this.$t('common.CANCEL'),
            buttonTrueColor: 'red lighten3',
            buttonFalseColor: 'yellow lighten3'
          }
        )
        if (response) {
          this.dataTableLoading = true
          await this.deleteBusiness(item._id)
          await this.getBusinesses(
            buildPayloadPagination(this.pagination, this.buildSearch())
          )
          this.dataTableLoading = false
        }
        // eslint-disable-next-line no-unused-vars
      } catch (error) {
        this.dataTableLoading = false
      }
    },
    close() {
      this.dialog = false
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
      }, 300)
    },
    async save() {
      try {
        // console.log('saving')
        const valid = await this.$validator.validateAll()
        if (valid) {
          this.dataTableLoading = true
          // Updating item
          if (this.editedItem._id) {
            await this.editBusiness(this.editedItem)
            await this.getBusinesses(
              buildPayloadPagination(this.pagination, this.buildSearch())
            )
            this.dataTableLoading = false
          } else {
            // Creating new item
            await this.saveBusiness({
              name: this.editedItem.name,
              email: this.editedItem.email,
              uri: this.editedItem.uri,
              businessType: this.editedItem.businessType,
              phone: this.editedItem.phone,
              streetAddress: this.editedItem.streetAddress,
              addressLocality: this.editedItem.addressLocality,
              addressRegion: this.editedItem.addressRegion,
              postalCode: this.editedItem.postalCode,
              contact: this.editedItem.contact,
              contactPhone: this.editedItem.contactPhone,
              contactEmail: this.editedItem.contactEmail,
              jobTitle: this.editedItem.jobTitle
            })
            await this.getBusinesses(
              buildPayloadPagination(this.pagination, this.buildSearch())
            )
            this.dataTableLoading = false
          }
          this.close()
          return
        }
        // eslint-disable-next-line no-unused-vars
      } catch (error) {
        this.dataTableLoading = false
        this.close()
      }
    }
  },
  async mounted() {
    await this.getAllCities()
  }
}
</script>

<style>
table.v-table {
  max-width: none;
}
</style>
